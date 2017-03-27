from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleCalenderWrapper(object):

    def __init__(self, event_count=10):
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'
        self.event_count = event_count

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def get_calender_list(service):
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'birthday' in calendar_list_entry.get('summary').lower():
                    return calendar_list_entry.get('id')
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return None

    def get_authorized_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        return discovery.build('calendar', 'v3', http=http)

    @staticmethod
    def get_events_list(service, calender_id):
        events_result = service.events().list(
            calendarId=calender_id,
            timeMin=datetime.utcnow().isoformat() + 'Z',
            maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', list())

    @staticmethod
    def convert_to_month_format(date_string):
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.strftime("%d %B %Y")

    def get_event_summary(self):
        service = self.get_authorized_service()
        birthday_calender_id = self.get_calender_list(service)
        events = self.get_events_list(service, birthday_calender_id)
        return [{'event': event.get('summary'),
                 'date': self.convert_to_month_format(
                                event['start'].get('dateTime', event['start'].get('date')))}
                for event in events]
