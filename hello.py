import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client


app = flask.Flask(__name__)


@app.route('/')
def index():
  print "1"
  if 'credentials' not in flask.session:
    print "2"
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  print "3"
  if credentials.access_token_expired:
    print "4"
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    print "5"
    http_auth = credentials.authorize(httplib2.Http())
    print "6"
    # drive_service = discovery.build('drive', 'v2', http_auth)
    # files = drive_service.files().list().execute()
    return 'authorized!'


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri='https://gcalendar-api-events.herokuapp.com/oauth2callback')
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()
