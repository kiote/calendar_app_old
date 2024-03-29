events_json = [{
  'summary': 'Programming Task',
  'location': 'http://www.path.to/study/website',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-09-28T06:00:00Z'
  },
  'end': {
    'dateTime': '2015-09-28T06:30:00Z'
  },
  'attendees': [
    {'email': 'study@studywebsite.com'}
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
},
{
  'summary': 'Programming Task 2',
  'location': 'http://www.path.to/study/website',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-09-29T06:00:00Z'
  },
  'end': {
    'dateTime': '2015-09-29T06:30:00Z'
  },
  'attendees': [
    {'email': 'study@studywebsite.com'}
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}]

event_json_changed = {
  'summary': 'Programming Task',
  'location': 'http://www.path.to/study/website',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-09-29T06:00:00Z'
  },
  'end': {
    'dateTime': '2015-09-29T06:30:00Z'
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'study@studywebsite.com'}
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
