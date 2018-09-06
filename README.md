# Mastodon Welcome Bot
This is a Mastodon bot that sends out a welcome toot (DM) to new users, brought to you by [jawns.club](https://jawns.club).  

Because Mastodon's API doesn't currently have a route for getting an array of accounts in an instance,
this bot queries the followers of an account and pages through for any have been created in the 
last x days (see configuration below). This means that you'll want `ACCOUNT_ID` to be an account
that is auto-followed by all new users.  

# Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/indyhall/mastodon-welcome-bot)


Hosting the bot on Heroku is probably the easiest (and cheapest, it's free!) way to go. There's only a few steps:

1. Click the button above. Once you're logged in to Heroku, you'll be taken to a window where you can set
the environment variables as detailed below. Then you can create the app.
2. Once the app is created, you'll have to schedule when it should run. Heroku's Scheduler addon is
used for this (don't worry, it's free). On your new app's page, click "Heroku Scheduler" under "Installed Add-ons". In the new window, set "python run.py" as the task to run and configure the schedule for the job. 

# Installation/Development  

Requires:

* python3
* pip

### Steps

1. `git clone git@github.com:indyhall/mastodon-welcome-bot.git`
2. `pip install -r requirements.txt` (you'll probably want to setup a [virtualenv](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) for this)
3. `cp .env.dist .env` 
4. Fill in the env vars as required in the `.env` file (see definitions below)
5. Run the app with `python run.py`

### Environment Variables

The application uses the following environment variables.  

| name              | required | default | description                                                                                                                                   |
|-------------------|----------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| ACCESS_TOKEN      | yes      | n/a     | the access token for the Mastodon account that you want the toots to come from                                                                |
| DAYS_SINCE        | no       | 1       | how many days back of new users you want to go                                                                                                |
| INSTANCE_BASE_URL | yes      | n/a     | the base url of the Mastodon instance you want to run this for (ex: "https://jawns.club")                                                     |
| TOOT_TEMPLATE     | yes      | n/a     | the template of the toot that you want to send out. [Jinja2](http://jinja.pocoo.org/) syntax is used here and you can use any of the [`Account`](https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md#account) variables                 |
| DEBUG             | no       | false   | boolean (either "true" or "false") for debug mode. If true, won't actually send out the toots, will just print the message for each to stdout |
| ACCOUNT_ID        | yes      | n/a     | the account ID that you want to pull followers from |
