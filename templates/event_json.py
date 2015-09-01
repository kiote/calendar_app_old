events_json = [{
  'summary': 'Programming Task',
  'location': 'http://www.path.to/study/website',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-09-28T18:00:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-09-28T18:30:00',
    'timeZone': 'America/Los_Angeles',
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
    'dateTime': '2015-09-29T18:00:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-09-29T18:30:00',
    'timeZone': 'America/Los_Angeles',
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
    'dateTime': '2015-09-29T18:00:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-09-29T18:30:00',
    'timeZone': 'America/Los_Angeles',
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
