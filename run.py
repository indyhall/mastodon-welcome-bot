from mastodon import Mastodon
from datetime import datetime, timedelta
import pytz
from environs import Env
from jinja2 import Template
import logging
import sys

class Bot(object):
    def __init__(self, access_token, since_at, instance_url, msg_template='', debug_mode=True, account_id=1):
        self.instance_url = instance_url
        self.msg_template = Template(msg_template)
        self.client = Mastodon(
            access_token=access_token,
            api_base_url=self.instance_url
        )
        self.since_at = since_at
        self.debug_mode = debug_mode

        self.log = logging.getLogger()
        if self.debug_mode:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        self.log.addHandler(ch)

        self.account_id = account_id

        self.until = pytz.utc.localize(datetime.now() - timedelta(days=1))
        self.until = self.until.replace(hour=23, minute=59, second=59)

    def _should_get_msg(self, account):
        return account.url.startswith(self.instance_url) and account.created_at >= self.since_at and account.created_at <= self.until and not account.locked

    def get_users(self):
        users_to_msg = []

        def get_prev(users):
            followers = self.client.fetch_previous(users)
            filtered = [follower for follower in followers if self._should_get_msg(follower)]
            users_to_msg.extend(filtered)

            # this assumes that followers are returned in descending order by follow date!
            if len(filtered) == 0:
                return users_to_msg

            return get_prev(followers)

        followers = self.client.account_followers(self.account_id, limit=80)
        filtered = [follower for follower in followers if self._should_get_msg(follower)]
        users_to_msg.extend(filtered)

        if len(filtered) == 0:
            return users_to_msg

        return get_prev(followers)

    def send_msg(self, account):
        msg = self.msg_template.render(account)
        msg = msg.replace('\\n', '\n')
        self.log.debug(msg)
        if self.debug_mode:
            return

        self.client.status_post(msg, visibility='private')

    def go(self):
        users_to_msg = self.get_users()
        if self.debug_mode:
            self.log.debug('in debug mode so not actually sending toots, but if I was, I\'d be sending to ' \
                  '{} accounts'.format(len(users_to_msg)))
            self.log.debug('here\'s the toots that I would be sending:')

        for u in users_to_msg:
            self.send_msg(u)

        self.log.info('{} toots sent!'. format(len(users_to_msg)))

def run():
    env = Env()
    env.read_env()
    access_token = env('ACCESS_TOKEN')
    days_since = env.int('DAYS_SINCE', 1)
    instance_base_url = env('INSTANCE_BASE_URL')
    msg_template = env('TOOT_TEMPLATE')
    debug_mode = env.bool('DEBUG', False)
    account_id = env.int('ACCOUNT_ID')

    since = pytz.utc.localize(datetime.now() - timedelta(days=days_since))
    bot = Bot(access_token,
              since_at=since,
              instance_url=instance_base_url,
              msg_template=msg_template,
              debug_mode=debug_mode,
              account_id=account_id)

    bot.go()

if __name__ == '__main__':
    run()
