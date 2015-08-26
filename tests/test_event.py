import unittest
from models.event import EventSaver
from templates.credentials_json import credentials_json


UserMock = {'email': 'dummy@test.com'}

class EventSaverTest(unittest.TestCase):
    def setUp(self):
        event_id = 'dummy_event_id'
        user_info = UserMock
        internal_event_id = 0
        self.subject = EventSaver(event_id, internal_event_id, user_info, credentials_json)

    def testExecutePushToQueue(self):
        self.subject.execute()


class EventCheckerTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
