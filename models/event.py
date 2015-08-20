from templates.event_json import event_json
from models.event_writer_structure import EventWriterStructure
from apiclient import discovery
from models.redis_conn import get_data_connection
from models.save_user import SaveUser
from rq import Queue
from redis.exceptions import ResponseError


class EventSaver:

    """Save created event to database."""

    def __init__(self, service, event_id, user_info):
        self.service = service
        self.event_id = event_id
        self.r = get_data_connection()
        self.user_info = user_info

    def execute(self):
        struct = EventWriterStructure("%s:%s" % (self.user_info['email'],
                                                 self.event_id))
        data_string = struct.get_data_string()
        # avoid adding one event several time
        self.r.lrem('unchecked', data_string, 0)
        self.r.lpush('unchecked', data_string)


class EventChecker:

    """Check if event beeing changed."""

    def __init__(self, event_structure, service):
        self.structure = event_structure
        self.service = service
        self.r = get_data_connection()

    def execute(self):
        event = self.service.events().get(calendarId='primary',
                                          eventId=self.structure.get_data_by_field_name('event_id')).execute()
        data_string = self.structure.get_data_string()
        self.r.lrem('unchecked', data_string, 0)
        if event['start']['dateTime'] != event_json['start']['dateTime']:
            self.r.lpush('checked', '%s:%d' % data_string, 1)
        else:
            self.r.lpush('checked', data_string)


class EventCreator:

    """Create event in GCalendar."""

    def __init__(self, http_auth, user_info):
        print http_auth
        self.service = discovery.build('calendar', 'v3', http=http_auth)
        self.user_info = user_info

    def execute(self):
        event_created = self.service.events().insert(calendarId='primary',
                                                     body=event_json).execute()

        EventSaver(self.service, event_created['id'], self.user_info).execute()
        return event_created
