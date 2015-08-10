from oauth2client import client

flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/drive.metadata.readonly',
    redirect_uri='https://gcalendar-api-events.herokuapp.com/oauth2callback')

auth_uri = flow.step1_get_authorize_url()

print auth_uri
