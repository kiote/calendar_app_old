import unittest
from models.event import EventSaver
from models.event import EventChecker
from templates.credentials_json import credentials_json
from templates.event_json import event_json_changed
from templates.event_json import events_json
from models.redis_conn import get_data_connection

import mock


UserMock = {'email': 'dummy@test.com'}

class ServiceMock:
    def __init__(self, changed):
        self.changed = changed

    def get(self, calendarId='', eventId=0):
        return self

    def execute(self):
        if self.changed:
            return event_json_changed
        else:
            return events_json[0]


class ServiceMockChangedEvent(ServiceMock):
    @staticmethod
    def events():
        return ServiceMock(True)


class ServiceMockUnchangedEvent(ServiceMock):
    @staticmethod
    def events():
        return ServiceMock(False)

class EventSaverTest(unittest.TestCase):
    def setUp(self):
        event_id = 'dummy_event_id'
        user_info = UserMock
        internal_event_id = 0
        self.subject = EventSaver(event_id, internal_event_id, user_info, credentials_json)

    def testExecutePushToQueue(self):
        self.subject.execute()


class EventCheckerTest(unittest.TestCase):
    def setUp(self):
        self.subject = EventChecker('test@sample.com|event_id|0|%s' % credentials_json)
        self.r = get_data_connection()
        self.r.flushall()

    @mock.patch('models.event.client')
    @mock.patch('models.event.discovery.build', lambda a, b, http='': ServiceMockChangedEvent(True))
    def test_execute_with_changed_event(self, client_mock):
        self.subject.execute()
        changed = self.r.lrange('changed', 0, -1)
        self.assertEquals(len(changed), 1)

    @mock.patch('models.event.client')
    @mock.patch('models.event.discovery.build', lambda a, b, http='': ServiceMockUnchangedEvent(True))
    def test_execute_with_unchanged_event(self, client_mock):
        self.subject.execute()
        changed = self.r.lrange('unchanged', 0, -1)
        self.assertEquals(len(changed), 1)


if __name__ == '__main__':
    unittest.main()
