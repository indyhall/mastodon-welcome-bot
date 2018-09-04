# Mastodon Welcome Bot
This is a Mastodon bot that sends out a welcome toot to new users, brought to you by [jawns.club](https://jawns.club).  

# Installation  

Requires:

* python3
* pip

Eventually this will be setup to as a "Deploy to Heroku" app, but for now:  

1. `git clone git@github.com:indyhall/mastodon-welcome-bot.git`
2. `pip install -r requirements.txt` (you'll probably want to setup a [virtualenv](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) for this)
3. `cp .env.dist .env` 
4. Fill in the env vars as required in the `.env` file (see definitions below)
5. Run the app with `python run.py`

# Usage

### Environment Variables

The application uses the following environment variables.  

| name              | required | default | description                                                                                                                                   |
|-------------------|----------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| ACCESS_TOKEN      | yes      | n/a     | the access token for the Mastodon account that you want the toots to come from                                                                |
| DAYS_SINCE        | no       | 1       | how many days back of new users you want to go                                                                                                |
| INSTANCE_BASE_URL | yes      | n/a     | the base url of the Mastodon instance you want to run this for (ex: "https://jawns.club")                                                     |
| TOOT_TEMPLATE     | yes      | n/a     | the template of the toot that you want to send out. Jinja2 syntax is used here and you can use any of the `Account` variables                 |
| DEBUG             | no       | false   | boolean (either "true" or "false") for debug mode. If true, won't actually send out the toots, will just print the message for each to stdout |
