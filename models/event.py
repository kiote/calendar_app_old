from templates.event import event
from apiclient import discovery

class Event:
    def __init__(self, http_auth):
        self.http_auth = http_auth

    def create_event(self):
        service = discovery.build('calendar', 'v3', http=self.http_auth)
        event_created = service.events().insert(calendarId='primary', body=event).execute()
        return event_created
