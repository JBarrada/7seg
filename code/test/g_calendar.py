import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import time
import argparse
import logging

logging.basicConfig(filename='GCAL_TEST.log', level=logging.INFO)

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

service = None
credentials = None

events = None
events_previous = None

color_ids = {}

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

def is_new_event(event):
    if events_previous:
        for previous_event in events_previous:
            if event["id"] == previous_event["id"]:
                return False
    return True

def update():
    global service, events, events_previous
    check_expired()
    events_previous = events

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    ten_days_from_now = (datetime.datetime.utcnow() + datetime.timedelta(days=10)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=ten_days_from_now,singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    new_events = 0
    if events:
        for event in events:
            if is_new_event(event):
                new_events += 1
    return new_events

def get_color_ids():
    global color_ids
    colors = service.colors().get().execute()
    for id in colors['event']:
        color_ids[id] = int(colors['event'][id]["background"][1:], 16)

def check_expired():
    global credentials, service
    if credentials.access_token_expired:
        logging.info(str(time.time())+" : TOKEN EXPIRED AND REFRESHED")
        credentials.refresh(httplib2.Http())
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        logging.info(credentials.to_json())

def init():
    global service, credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    logging.info(credentials.to_json())
    get_color_ids()

clocknext = 0

seconds = 0
init()
while True:
    if time.clock() >= clocknext:
        clocknext = time.clock() + 1
        logging.info("EXPIRED?? %s" % credentials.access_token_expired)
        logging.info("TIME:: %d  DATETIME:: %s" % (seconds, datetime.datetime.now().strftime("%H:%M:%S")))
        print("TIME:: %d" % seconds)
        update()
        logging.info("UPDATED")
        logging.info("------------------------------------")
        seconds += 1

