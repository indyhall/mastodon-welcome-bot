from mastodon import Mastodon
from datetime import datetime, timedelta
import pytz
from environs import Env
from jinja2 import Template

class Bot(object):
    def __init__(self, access_token, since_at, instance_url, msg_template='', debug_mode=False):
        self.instance_url = instance_url
        self.msg_template = Template(msg_template)
        self.client = Mastodon(
            access_token=access_token,
            api_base_url=self.instance_url
        )
        self.since_at = since_at
        self.debug_mode = debug_mode

    def _should_get_msg(self, account):
        return account.url.startswith(self.instance_url) and account.created_at >= self.since_at and not account.locked

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

        followers = self.client.account_followers(1, limit=80)
        filtered = [follower for follower in followers if self._should_get_msg(follower)]
        users_to_msg.extend(filtered)

        if len(filtered) == 0:
            return users_to_msg

        return get_prev(followers)

    def send_msg(self, account):
        msg = self.msg_template.render(account)
        if self.debug_mode:
            print(msg)
            return

        # self.client.status_post(msg, visibility='private')


    def go(self):
        users_to_msg = self.get_users()
        if self.debug_mode:
            print('in debug mode so not actually sending toots, but if I was, I\'d be sending to ' \
                  '{} accounts'.format(len(users_to_msg)))
            print('Here\'s the toots that I would have been sending:')

        for u in users_to_msg:
            self.send_msg(u)

        if not self.debug_mode:
            print('{} toots sent!'. format(len(users_to_msg)))

def run():
    env = Env()
    env.read_env()
    access_token = env('ACCESS_TOKEN')
    days_since = env.int('DAYS_SINCE', 1)
    instance_base_url = env('INSTANCE_BASE_URL')
    msg_template = env('TOOT_TEMPLATE')
    debug_mode = env.bool('DEBUG', False)

    since = pytz.utc.localize(datetime.now() - timedelta(days=days_since))
    bot = Bot(access_token,
              since_at=since,
              instance_url=instance_base_url,
              msg_template=msg_template,
              debug_mode=debug_mode)

    bot.go()

if __name__ == '__main__':
    run()
