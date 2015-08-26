from templates.event_json import events_json
from apiclient import discovery
from models.redis_conn import get_data_connection
from oauth2client import client
import httplib2
import traceback

class UncheckedEvent:
    def __init__(self, event_id, internal_event_id, email, credentials):
        self.event_id = event_id
        self.internal_event_id = internal_event_id
        self.credentials = credentials
        self.email = email

    def __str__(self):
        return "%s|%s|%s|%s" % (self.email,
                                self.event_id,
                                self.internal_event_id,
                                self.credentials)


class CheckedEvent:
    def __init__(self, event_id, user_info, event_name):
        self.event_id = event_id
        self.user_info = user_info
        self.event_name = event_name

    def __str__(self):
        return "%s|%s|%s" % (self.user_info['email'],
                             self.event_id,
                             self.event_name)

class EventSaver:

    """
    Save just created by user event to database.

    We add this events to "unchecked" queue (redis array).
    """

    def __init__(self, event_id, internal_event_id, user_info, credentials):
        self.event_id = event_id
        self.internal_event_id = internal_event_id
        self.credentials = credentials
        self.user_info = user_info
        self.r = get_data_connection()

    def execute(self):
        data_string = str(UncheckedEvent(self.event_id,
                                         self.internal_event_id,
                                         self.user_info['email'],
                                         self.credentials))
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
        splitted = event.split('|')

        self.email = splitted[0]
        self.event_id = splitted[1]
        self.internal_event_id = splitted[2]
        self.credentials = "".join(splitted[3:])
        self.r = get_data_connection()

    def execute(self):
        try:
            credentials = client.OAuth2Credentials.from_json(self.credentials)
            http_auth = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http_auth)
            event = service.events().get(calendarId='primary',
                                         eventId=self.event_id).execute()
            self.r.lrem('unchecked', str(UncheckedEvent(self.event_id, self.internal_event_id, self.email, self.credentials)), 0)
            internal_event = events_json[int(self.internal_event_id)]
            if event['start']['dateTime'] != internal_event['start']['dateTime']:
                self.r.lpush('changed', str(CheckedEvent(self.event_id, self.email, internal_event['summary'])))
            else:
                self.r.lpush('unchanged', str(CheckedEvent(self.event_id, self.email, internal_event['summary'])))
        except:
            print traceback.format_exc()


class EventList:

    """Return list of changed/unchanged events"""

    def __init__(self):
        self.r = get_data_connection()

    def get(self):
        unchanged = self.r.lrange('unchanged', 0, -1)
        changed = self.r.lrange('changed', 0, -1)
        return unchanged, changed

class EventCreator:

    """Create event in GCalendar."""

    def __init__(self, http_auth, event_id):
        self.service = discovery.build('calendar', 'v3', http=http_auth)
        self.event_id = event_id

    def execute(self):
        event_json = events_json[self.event_id]
        event_created = self.service.events().insert(calendarId='primary',
                                                     body=event_json).execute()
        return event_created
