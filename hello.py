import json
import sys, traceback
import uuid

from flask import Flask, session, redirect, url_for, escape, request
import httplib2

from apiclient import discovery
from oauth2client import client


app = Flask(__name__)


@app.route('/')
def index():
  if 'credentials' not in session:
    return redirect(url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(session['credentials'])
  if credentials.access_token_expired:
    return redirect(url_for('oauth2callback'))
  else:
    try:
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        event = {
          'summary': 'Programming Task',
          'location': 'http://www.path.to/study/website',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '2015-09-28T18:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2015-09-28T18:30:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
          ],
          'attendees': [
            {'email': 'study@studywebsite.com'}
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return 'Event created, you can edit it <a herf="%s">here</a>' % (event.get('htmlLink'))
    except:
        return traceback.format_exc()


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri='https://gcalendar-api-events.herokuapp.com/oauth2callback')
  if 'code' not in request.args:
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)
  else:
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    try:
        session['credentials'] = credentials.to_json()
    except:
        print traceback.format_exc()
    return redirect(url_for('index'))


app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = str(uuid.uuid4())

if __name__ == '__main__':
  app.debug = True
  app.run()
