import unittest
from models.event import EventSaver
from templates.event_json import event_json_changed
from templates.credentials_json import credentials_json


class ServiceMock:
    def events(self):
        return self

    def get(self, calendarId='', eventId=''):
        return self

    def execute(self):
        return event_json_changed

UserMock = {'email': 'dummy@test.com'}

class EventSaverTest(unittest.TestCase):
    def setUp(self):
        service = ServiceMock()
        event_id = 'dummy_event_id'
        user_info = UserMock
        self.subject = EventSaver(event_id, user_info, credentials_json)

    def testExecutePushToQueue(self):
        self.subject.execute()


if __name__ == '__main__':
    unittest.main()
