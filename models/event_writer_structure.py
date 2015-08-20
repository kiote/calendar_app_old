from collections import namedtuple

class EventWriterStructure:
    def __init__(self, data):
        EventData = namedtuple('EventData', 'email, event_id')
        self.data_str = data
        email, event_id = self._unpack()
        self.data = EventData(email, event_id)

    def _unpack(self):
        res = self.data_str.split(':')

        return res[0], res[1]

    def get_data_by_field_name(self, name):
        return getattr(self.data, name)

    def get_data_string(self):
        return self.data_str
