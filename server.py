import json
from apiclient import errors
import logging
import traceback
import uuid

from flask import Flask, session, redirect, url_for, request, render_template
import httplib2

from oauth2client import client

from models.event import EventCreator
from models.event import EventSaver
from models.event import EventList
from models.email import Email

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar', 'email', 'profile']


@app.route('/addevent/<int:event_id>')
def add_event(event_id):
    try:
        if 'credentials' not in session:
            return redirect(url_for('oauth2callback'))
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        if credentials.access_token_expired:
            return redirect(url_for('oauth2callback'))
        http_auth = credentials.authorize(httplib2.Http())
        user_info = Email(http_auth).discover_user()
        event_created = EventCreator(http_auth, event_id).execute()

        EventSaver(event_created['id'], event_id, user_info, session['credentials']).execute()

        return render_template('event.html', event_url=event_created.get('htmlLink'))
    except:
        return traceback.format_exc()


@app.route('/stat')
def stat():
    try:
        unchanged, changed = EventList().get()

        return render_template('stat.html',
                               unchanged=unchanged,
                               changed=changed)
    except:
        return traceback.format_exc()

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        return render_template('events.html')

@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope=' '.join(SCOPES),
      redirect_uri='https://gcalendar-api-events.herokuapp.com/oauth2callback')
  if 'code' not in request.args:
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)
  else:
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    try:
        session['credentials'] = credentials.to_json()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)
    return redirect(url_for('index'))


app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = str(uuid.uuid4())

if __name__ == '__main__':
    app.debug = True
    app.run()
