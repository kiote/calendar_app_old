![](https://travis-ci.org/kiote/calendar_app.svg?branch=master)

# Work with Google Calendar API

This app is a simple example of using Google Calendar API.

It uses Flask under the hood.

To be able to run tests locally:

    export REDIS_URL='127.0.0.1:6379'
    export PYTHONPATH=.

You should have Redis server up and running.

# Installation

1. Install [Redis](redis.com)
2. Install application requirements with
    ```pip install -r requirements.txt```
3. Run Redis (see Redis doc to run it dependin on your OS)
4. Run application: ```python server.py```
5. Create a cron job to run worker.py every 10 minutes with ```python worker.py``` command
