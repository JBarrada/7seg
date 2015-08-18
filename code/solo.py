import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = '7SEG'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, '7seg.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.params['access_type'] = 'offline'
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

        print 'Storing credentials to ' + credential_path
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
print 'Getting the upcoming 10 events'
eventsResult = service.events().list(
    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
events = eventsResult.get('items', [])

if not events:
    print 'No upcoming events found.'
for event in events:
    start = event['start'].get('dateTime')
    title = event['summary']
    colorid = event['colorId']

    print('start: %s\t title: %s\t colorid: %s' % (start, title, colorid))
