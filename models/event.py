from templates.event_json import event_json
from apiclient import discovery
from models.redis_conn import get_data_connection
from oauth2client import client
import httplib2

class EventSaver:

    """
    Save just created by user event to database.

    We add this events to "unchecked" queue (redis array).
    """

    def __init__(self, event_id, user_info, credentials):
        self.event_id = event_id
        self.credentials = credentials
        self.user_info = user_info
        self.r = get_data_connection()

    def execute(self):
        data_string = "%s:%s:%s" % (self.user_info['email'],
                                    self.event_id,
                                    self.credentials)
        # avoid adding one event several time
        self.r.lrem('unchecked', data_string, 0)
        self.r.lpush('unchecked', data_string)


class EventChecker:

    """
    Check if event had been changed.

    Remove it from "unchecked" queue and add either to "changed" or "unchanged"
    queues (redis arrays).
    """

    def __init__(self, event):
        self.event = event
        splitted = event.split(':')
        self.email = splitted[0]
        self.event_id = splitted[1]
        self.credentials = splitted[2]
        self.r = get_data_connection()

    def execute(self):
        credentials = client.OAuth2Credentials.from_json(self.credentials)
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        event = service.events().get(calendarId='primary',
                                     eventId=self.event_id).execute()
        self.r.lrem('unchecked', self.event, 0)
        if event['start']['dateTime'] != event_json['start']['dateTime']:
            self.r.lpush('changed', self.event)
        else:
            self.r.lpush('unchanged', self.event)


class EventCreator:

    """Create event in GCalendar."""

    def __init__(self, http_auth):
        self.service = discovery.build('calendar', 'v3', http=http_auth)

    def execute(self):
        event_created = self.service.events().insert(calendarId='primary',
                                                     body=event_json).execute()
        return event_created
