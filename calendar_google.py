from __future__ import print_function
import datetime
import os.path
import sys
from re import S
import socket
socket.setdefaulttimeout(4000)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from PySide2.QtCore import QThread
from PySide2.QtGui import *
from PySide2.QtCore import *

import menu
from recipe import Recipe

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


def quickstart():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def build_service(debug = False):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    if debug:
        print('service built')
    return service

def getTimeZone(service, debug = False):
    calendar = service.calendars().get(calendarId='primary').execute()
    timeZone = calendar['timeZone']
    if debug:
        print('time zone detected')
    return timeZone

def createCalendar(service, timeZone, debug = False):
    id = existingCalendarID(service, 'À Table!')
    if id == 0:
        # print('creating secondary calendar for the first time')
        calendar = {
        'summary': 'À Table!',
        'timeZone': timeZone#,
        # 'colorRgbFormat' : 'True',
        # 'backgroundColor' : '#0088aa',
        # 'foregroundColor' : '#ffffff'
        }
        
        created_calendar = service.calendars().insert(body=calendar).execute()
        
        # get the corresponding ID
        if debug:
            print('calendar created')
        id = created_calendar['id']
    elif debug:
        print('existing calendar found')
    return id

def build_event(timeZone, title = 'New Event', description = 'event content', start = None, end = None, debug = False):
    if start is None:
        start = datetime.datetime.utcnow()
    start_iso = start.isoformat() #+ 'Z'
    if end is None:
        end = start + datetime.timedelta(hours = 1)
    end_iso = end.isoformat() #+ 'Z'
    
    event = {
    'summary': title,
    'description': description,
    'start': {
        'dateTime': start_iso,
        'timeZone': timeZone,
    },
    'end': {
        'dateTime': end_iso,
        'timeZone': timeZone,
    },
    }
    if debug:
        print('event built')
    return event
    
def add_event(service, id, event, debug = False):
    event = service.events().insert(calendarId=id, body=event).execute()
    link = event.get('htmlLink')
    if debug:
        print('Event created: %s' % (link))
    return link

def add_event_standalone(title = 'New Event', description = 'event content', start = None, end = None):
    """Add an event to the user's calendar with the Google Calendar API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() #+ 'Z' # 'Z' indicates UTC time
    
    calendar = service.calendars().get(calendarId='primary').execute()
    timeZone = calendar['timeZone']
    
    #create dedicated secondary calendar "a table" the first time an event is created
    id = existingCalendarID(service, 'À Table!')
    if id == 0:
        # print('creating secondary calendar for the first time')
        calendar = {
        'summary': 'À Table!',
        'timeZone': timeZone#,
        # 'colorRgbFormat' : 'True',
        # 'backgroundColor' : '#0088aa',
        # 'foregroundColor' : '#ffffff'
        }
        
        created_calendar = service.calendars().insert(body=calendar).execute()
        
        # get the corresponding ID
        id = created_calendar['id']
    # else:
    #     print('secondary calendar already exists')
        
    if start is None:
        start = datetime.datetime.utcnow()
    start_iso = start.isoformat() #+ 'Z'
    if end is None:
        end = start + datetime.timedelta(hours = 1)
    end_iso = end.isoformat() #+ 'Z'
    
    event = {
    'summary': title,
    # 'location': '800 Howard St., San Francisco, CA 94103',
    'description': description,
    'start': {
        # 'dateTime': '2021-09-09T09:00:00-07:00',
        # 'dateTime': '2021-09-09T09:00:00',
        'dateTime': start_iso,
        'timeZone': timeZone,
    },
    'end': {
        # 'dateTime': '2021-09-09T17:00:00-07:00',
        # 'dateTime': '2021-09-09T17:00:00',
        'dateTime': end_iso,
        'timeZone': timeZone,
    },
    # 'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    # ],
    # 'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    # ],
    # 'reminders': {
    #     'useDefault': False,
    #     'overrides': [
    #     {'method': 'email', 'minutes': 24 * 60},
    #     {'method': 'popup', 'minutes': 10},
    #     ],
    # },
    }


    # event = service.events().insert(calendarId='primary', body=event).execute()
    event = service.events().insert(calendarId=id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



def get_calendar_list(service):
    page_token = None
    calendar_summary_list = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendar_summary_list.append((calendar_list_entry['summary'], calendar_list_entry['id']))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    # print(calendar_summary_list)
    return calendar_summary_list

def existingCalendarID(service, summary):
    calendar_summary_list = get_calendar_list(service)
    for title, id in calendar_summary_list:
        # print('%s-%s' % (title, summary))
        if title == summary:
            return id
    return 0

class MySignal(QObject):
    sig = Signal(str, str)

class MyCalendar(QThread):#QThread
    def __init__(self, my_menu):
        QThread.__init__(self)
        self.menu = my_menu
        self.signal = MySignal()
        self.dirname = os.path.dirname(__file__)
        self.icon_path = self.dirname + '/UI/images/icon_calendar.png'
        
    def run(self):
        debug = True
        self.signal.sig.emit('La céation des évènements est en cours...', self.icon_path)
        try:
            service = self.build_service(debug=debug)
            timeZone = self.getTimeZone(service, debug=debug)
            id = self.createCalendar(service, timeZone, debug=debug)
            
            message = ''
            menu_list = self.menu.table
            start_day = self.menu.start_day
            nb_of_days = self.menu.number_of_days
            
            for d in range(nb_of_days):
                start_lunch = datetime.datetime(start_day.year, 
                                        start_day.month, 
                                        start_day.day + d,
                                        12)
                start_dinner = datetime.datetime(start_day.year, 
                                        start_day.month, 
                                        start_day.day + d,
                                        19)
                
                recipe_lunch  = menu_list[2*d]
                recipe_dinner = menu_list[2*d+1]
                
                if type(recipe_lunch) == Recipe:
                    recipe_lunch_stack = [recipe_lunch]
                elif type(recipe_lunch) == list:
                    recipe_lunch_stack = recipe_lunch
                
                if type(recipe_dinner) == Recipe:
                    recipe_dinner_stack = [recipe_dinner]
                elif type(recipe_dinner) == list:
                    recipe_dinner_stack = recipe_dinner
                
                title_lunch  = ' | '.join([recipe_lunch.name 
                                           for recipe_lunch in recipe_lunch_stack])
                
                description_lunch = ''
                for recipe_lunch in recipe_lunch_stack:
                    description_lunch += '<br/><b>%s</b><br/>' % recipe_lunch.name
                    description_lunch += '<br/>'.join(recipe_lunch.ingredients_string_list())
                    description_lunch += '<br/>%s<br/>' % recipe_lunch.preparation
                
                title_dinner = ' | '.join(recipe_dinner.name 
                                          for recipe_dinner in recipe_dinner_stack)
                
                description_dinner = ''
                for recipe_dinner in recipe_dinner_stack:
                    description_dinner += '<br/><b>%s</b><br/>' % recipe_dinner.name
                    description_dinner += '<br/>'.join(recipe_dinner.ingredients_string_list())
                    description_dinner += '<br/>%s<br/>' % recipe_dinner.preparation
                
                
                event_lunch  = self.build_event(timeZone, title_lunch,  description_lunch,  start_lunch, debug=True)
                event_dinner = self.build_event(timeZone, title_dinner, description_dinner, start_dinner, debug=True)
                
                link_lunch  = self.add_event(service, id, event_lunch, debug=True)
                link_dinner = self.add_event(service, id, event_dinner, debug=True)
                
                # message += '%s :\n' % menu.full_date_to_french(start_lunch)
                # message += 'Midi : %s - %s\n' % (title_lunch, link_lunch)
                # message += 'Soir : %s - %s\n' % (title_dinner, link_dinner)
            message += "%i nouveaux évènements créés dans l'agenda<br/>" % (nb_of_days*2)
            message += '<a href="%s">Lien Google Calendar</a>' % link_dinner
            
            self.signal.sig.emit(message, self.icon_path)
        except:
            self.signal.sig.emit("Le calendrier n'est pas accessible (Request Time Out)", self.icon_path)
            print(sys.exc_info())

    def build_service(self, debug = False):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        if debug:
            print('service built')
        return service

    def getTimeZone(self, service, debug = False):
        calendar = service.calendars().get(calendarId='primary').execute()
        timeZone = calendar['timeZone']
        if debug:
            print('time zone detected')
        return timeZone

    def createCalendar(self, service, timeZone, debug = False):
        id = existingCalendarID(service, 'À Table!')
        if id == 0:
            # print('creating secondary calendar for the first time')
            calendar = {
            'summary': 'À Table!',
            'timeZone': timeZone#,
            # 'colorRgbFormat' : 'True',
            # 'backgroundColor' : '#0088aa',
            # 'foregroundColor' : '#ffffff'
            }
            
            created_calendar = service.calendars().insert(body=calendar).execute()
            
            # get the corresponding ID
            if debug:
                print('calendar created')
            id = created_calendar['id']
        elif debug:
            print('existing calendar found')
        return id

    def build_event(self, timeZone, title = 'New Event', description = 'event content', start = None, end = None, debug = False):
        if start is None:
            start = datetime.datetime.utcnow()
        start_iso = start.isoformat() #+ 'Z'
        if end is None:
            end = start + datetime.timedelta(hours = 1)
        end_iso = end.isoformat() #+ 'Z'
        
        event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_iso,
            'timeZone': timeZone,
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': timeZone,
        },
        }
        if debug:
            print('event built')
        return event
        
    def add_event(self, service, id, event, debug = False):
        event = service.events().insert(calendarId=id, body=event).execute()
        link = event.get('htmlLink')
        if debug:
            print('Event created: %s' % (link))
        return link

if __name__ == '__main__':
    # add_event_standalone(title='Hello', description='tout va bien', start= datetime.datetime(2021,9,10,11))
    try:
        service = build_service(debug=True)
        timeZone = getTimeZone(service, debug=True)
        id = createCalendar(service, timeZone, debug=True)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    
    