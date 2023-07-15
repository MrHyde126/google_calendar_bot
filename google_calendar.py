import os.path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
BIRTHDAYS_ID = 'addressbook#contacts@group.v.calendar.google.com'
HOLIDAYS_ID = 'ru.russian#holiday@group.v.calendar.google.com'


class GoogleCalendar:
    def __init__(self):
        self.service = build('calendar', 'v3', credentials=self._get_creds())

    def _get_creds(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_events_list(self, id):
        now = datetime.now().isoformat() + 'Z'
        events_result = (
            self.service.events()
            .list(
                calendarId=id,
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])
        if not events:
            return 'Предстоящих событий не найдено.'
        event_list = ''
        for event in events:
            start = event['start'].get('date')
            year = start[:4]
            month = start[5:7]
            day = start[-2:]
            date = f'{day}.{month}.{year}'
            cur_event = f'{date}  {event["summary"]}\n'
            event_list += cur_event
        return event_list

    def get_today_events(self):
        now = datetime.now().isoformat() + 'Z'
        events_result = (
            self.service.events()
            .list(
                calendarId=BIRTHDAYS_ID,
                timeMin=now,
                timeMax=(datetime.now() + timedelta(hours=1)).isoformat()
                + 'Z',
                singleEvents=True,
            )
            .execute()
        )
        events = events_result.get('items', [])
        if not events:
            return None
        event_list = 'Сегодня:\n'
        for event in events:
            event_list += f'{event["description"]}\n'
        return event_list
