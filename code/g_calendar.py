import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

service = None
pending_events = 0
high_priority = 0

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, '7seg.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('secrets.json', 'https://www.googleapis.com/auth/calendar.readonly')
        flow.params['access_type'] = 'offline'
        flow.user_agent = '7SEG'

        credentials = tools.run_flow(flow, store, flags)

        print 'Storing credentials to ' + credential_path
    return credentials

def update():
    global service, pending_events, high_priority
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    ten_days_from_now = (datetime.datetime.utcnow() + datetime.timedelta(days=10)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=ten_days_from_now,singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        pending_events = 0
    else:
        high_priority = 0
        for event in events:
            print(event["summary"])
            if "URGENT" in event["summary"]:
                high_priority += 1
        pending_events = len(events)


def init():
    global service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

