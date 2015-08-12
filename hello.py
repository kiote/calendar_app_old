import json
import sys, traceback

from flask import Flask, session, redirect, url_for, escape, request
import httplib2

from apiclient import discovery
from oauth2client import client


app = Flask(__name__)


@app.route('/')
def index():
  if 'credentials' not in session:
    return redirect(url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return redirect(url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    # drive_service = discovery.build('drive', 'v2', http_auth)
    # files = drive_service.files().list().execute()
    return 'authorized!'


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
        traceback.format_exc()
    return redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()
