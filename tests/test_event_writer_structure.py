import unittest

from models.event_writer_structure import EventWriterStructure


class EventWriterStructureTest(unittest.TestCase):
    def setUp(self):
        self.data_str = 'dummy@test.com:some_event_id'
        self.subject = EventWriterStructure(self.data_str)

    def testSetParamsCorrectly(self):
        self.assertEqual(self.subject.get_data_by_field_name('email'), 'dummy@test.com')
        self.assertEqual(self.subject.get_data_by_field_name('event_id'), 'some_event_id')

    def testGetDataStr(self):
        self.assertEqual(self.subject.get_data_string(), self.data_str)

if __name__ == '__main__':
    unittest.main()
