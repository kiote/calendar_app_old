from templates.event_json import event_json
from apiclient import discovery
from models.redis_conn import get_connection
from rq import Queue


class EventChecker:
    """Check event for existance."""
    def __init__(self, service, event_id):
        self.service = service
        self.event_id = event_id

    def execute(self):
        """Send check event job to queue."""
        redis_conn = get_connection()
        q = Queue(connection=redis_conn)
        q.enqueue(self._check_event)

    def _check_event(self):
        """
        Check, if event were changed.

        This function supposed to be run delayed.
        """
        event = self.service.events().get(calendarId='primary',
                                          eventId=self.event_id).execute()
        # if event time != event_json time we need to write to redis
        # changed flag


class EventCreator:
    """Create event.""""
    def __init__(self, http_auth):
        self.service = discovery.build('calendar', 'v3', http=http_auth)

    def execute(self):
        """Create event in GCalendar."""
        event_created = self.service.events().insert(calendarId='primary',
                                                     body=event_json).execute()

        EventChecker(self.service, event_created['id']).execute()
        return event_created
