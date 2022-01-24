from __future__ import print_function
import datetime
import os
import sys
from re import S
import socket

from httplib2 import debuglevel
socket.setdefaulttimeout(4000)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

import lxml.html
from os.path import basename
import base64

from PySide2.QtCore import QThread
from PySide2.QtGui import *
from PySide2.QtCore import *

import menu
import re
from recipe import Recipe
import custom_widgets as cw

import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 
          'https://www.googleapis.com/auth/calendar.events', 
          'https://www.googleapis.com/auth/gmail.insert']

def get_credentials(debug = False):
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
    
    if debug:
        print(creds)
    
    return creds

def build_calendar_service(creds, debug = False):
    service = build('calendar', 'v3', credentials=creds)
    if debug:
        print('service built for calendar')
    return service

def build_gmail_service(creds, debug = False):
    service = build('gmail', 'v1', credentials=creds)
    if debug:
        print('service built for gmail')
    return service

def getTimeZone(service, debug = False):
    calendar = service.calendars().get(calendarId='primary').execute()
    timeZone = calendar['timeZone']
    if debug:
        print('time zone detected')
    return timeZone

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

def build_message(fromaddr, toaddr, subject, message, files = None):
    msg = MIMEMultipart('related')
    # msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)

    for f in files or []:
        if f[-3:] == 'png':#attach image for html cid reference
            with open(f, 'rb') as fil:
                msgimage = MIMEImage(fil.read())
            msgimage.add_header('Content-ID', '<%s>' %(basename(f)))
            msg.attach(msgimage)
        else:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    
    b64_bytes = base64.urlsafe_b64encode(msg.as_bytes())
    b64_string = b64_bytes.decode()
    body = {'raw': b64_string,
            "labelIds": ['INBOX', 'UNREAD']}
    return body

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    # data_string = message.as_string()
    # print(data_string)
    # data_bytes = data_string.encode("utf-8")
    # return {'raw': base64.urlsafe_b64encode(message.as_string())}
    # return {'raw': base64.urlsafe_b64encode(data_bytes)}
    
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    body = {'raw': b64_string,
            "labelIds": ['INBOX', 'UNREAD']}
    return body
    # return {'raw': base64.urlsafe_b64encode(message)}
    # return {'raw': data_string}

def create_message_with_attachment(
    sender, to, subject, message_text, file):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    # data_string = message.as_string()
    # data_bytes = data_string.encode("utf-8")
    # # return {'raw': base64.urlsafe_b64encode(message.as_string())}
    # # return {'raw': base64.urlsafe_b64encode(data_bytes)}
    # return {'raw': data_string}
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    body = {'raw': b64_string,
            "labelIds": ['INBOX', 'UNREAD']}
    return body

def insert_message(service, user_id, message):
    """Insert an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
#   try:
    message = service.users().messages().insert(userId=user_id, body=message).execute()
    # print('Message Id: %s' % message['id'])
    return message
#   except:
#     print(sys.exc_info())

def replace_multiple(string, from_to_dict):
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in from_to_dict.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
    return text

def is_internet_available():
    url = "https://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

class MyCalendar(QThread):#QThread
    
    on_message = Signal(str, str)
    on_finish = Signal()
    
    def __init__(self, my_menu):
        QThread.__init__(self)
        self.menu = my_menu
        self.icon_path = cw.dirname('UI/images') + 'icon_calendar.png'
        self.occurences = 0
        
    def run(self):
        debug = True
        # self.signal.sig.emit('La céation des évènements est en cours...', self.icon_path)
        
        if is_internet_available():
        
            self.on_message.emit('La céation des évènements est en cours...', self.icon_path)
            
            try:
                creds = get_credentials(debug=debug)
                service = build_calendar_service(creds, debug=debug)
                timeZone = getTimeZone(service, debug=debug)
                id = createCalendar(service, timeZone, debug=debug)
                
                message = ''
                menu_list = self.menu.table
                start_day = self.menu.start_day
                nb_of_days = self.menu.number_of_days
                
                for d in range(nb_of_days):
                    start_lunch = datetime.datetime(start_day.year, 
                                            start_day.month, 
                                            start_day.day,
                                            12) + datetime.timedelta(days = d)
                    start_dinner = datetime.datetime(start_day.year, 
                                            start_day.month, 
                                            start_day.day,
                                            19) + datetime.timedelta(days = d)
                    
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
                        if len(recipe_lunch.ingredients_string_list()) > 0:
                            description_lunch += '<br/><i>Ingrédients</i><br/>'
                            description_lunch += '<br/>'.join(recipe_lunch.ingredients_string_list())
                        if recipe_lunch.preparation != '':
                            description_lunch += '<br/><i>Préparation</i><br/>'
                            description_lunch += '<br/>%s<br/>' % recipe_lunch.preparation
                    
                    title_dinner = ' | '.join(recipe_dinner.name 
                                            for recipe_dinner in recipe_dinner_stack)
                    
                    description_dinner = ''
                    for recipe_dinner in recipe_dinner_stack:
                        description_dinner += '<br/><b>%s</b><br/>' % recipe_dinner.name
                        if len(recipe_dinner.ingredients_string_list()) > 0:
                            description_dinner += '<br/><i>Ingrédients</i><br/>'
                            description_dinner += '<br/>'.join(recipe_dinner.ingredients_string_list())
                        if recipe_dinner.preparation != '':
                            description_dinner += '<br/><i>Préparation</i><br/>'
                            description_dinner += '<br/>%s<br/>' % recipe_dinner.preparation
                    
                    
                    event_lunch  = build_event(timeZone, title_lunch,  description_lunch,  start_lunch, debug=debug)
                    event_dinner = build_event(timeZone, title_dinner, description_dinner, start_dinner, debug=debug)
                    
                    link_lunch  = add_event(service, id, event_lunch, debug=debug)
                    link_dinner = add_event(service, id, event_dinner, debug=debug)
                    
                    # message += '%s :\n' % menu.full_date_to_french(start_lunch)
                    # message += 'Midi : %s - %s\n' % (title_lunch, link_lunch)
                    # message += 'Soir : %s - %s\n' % (title_dinner, link_dinner)
                message += "%i nouveaux évènements créés dans l'agenda<br/>" % (nb_of_days*2)
                message += '<a href="%s">Lien Google Calendar</a>' % link_dinner
                
                # self.signal.sig.emit(message, self.icon_path)
                self.on_message.emit(message, self.icon_path)

            except:
                if self.occurences < 2:
                    print('Request failed, trying to regenerate token with authorization process...')
                    #delete token.json and run again
                    if os.path.exists('token.json'):
                        os.remove('token.json')
                    #increment occurences
                    self.occurences += 1
                    self.run()
                else:
                    # self.signal.sig.emit("Le calendrier n'est pas accessible (Request Time Out)", self.icon_path)
                    self.on_message.emit("Le calendrier n'est pas accessible (Request Time Out)", self.icon_path)
                    
                    print(sys.exc_info())
        
        else:
            self.on_message.emit('Pas de connection à Internet !<br/>'
                                 + "Les menus n'ont pas pu être copiés dans l'agenda", '')
        
        self.on_finish.emit()

class MyMailbox(QThread):
    
    CORE_SHOPPING_HTML = cw.dirname('') + 'shopping_core.html'
    CORE_RECIPE_HTML = cw.dirname('') + 'recipe_core.html'
    on_message = Signal(str, str)

    def __init__(self, option, list_args):
        QThread.__init__(self)
        self.sender = 'notification.a.table@gmail.com'
        self.option = option
        self.occurences = 0
        
        if self.option == 'shopping':
            my_menu, to_email, images, images_dict = list_args
            
            self.my_menu = my_menu#<-
            self.to_email = to_email#<-
            self.images = images#<-
            self.images_dict = images_dict#<-
        
        elif self.option == 'recipe':
            recipe, to_email, images, images_dict, pdf = list_args
            
            self.recipe = recipe
            self.to_email = to_email
            self.images = images
            self.images_dict = images_dict
            self.pdf = pdf
            
        self.icon_path = cw.dirname('UI/images') + '/UI/images/icon_send.png'
        
    
    def run(self):
        if self.option == 'shopping':
            self.send_shopping_list(self.my_menu, self.to_email, self.images, self.images_dict)

        elif self.option == 'recipe':
            self.send_recipe(self.recipe, self.to_email, self.images, self.images_dict, self.pdf)
    
    def send_recipe(self, recipe, to_email, images, images_dict, pdf):
        # print('send recette')
        TITLE = recipe.name
        subject = 'Fiche recette - %s' % TITLE

        with open(self.CORE_RECIPE_HTML, 'r') as f:
            data = f.readlines()
        
        core_text = ''.join(map(str.strip, data))

        rep = {'[TITLE]': TITLE} #define desired replacements here
        
        
        text = replace_multiple(core_text, rep)
        html_body = replace_multiple(text, images_dict)
        
        self.send(to_email, subject, html_body, files = images + [pdf])
    
    def send_shopping_list(self, my_menu, to_email, images, images_dict):
        #create email body in HTML containing full menu and shopping list
        '''
        [TITLE]
        [ICON_MENU_PATH] #to be replaced within GUI class
        [TABLE_DAYS]
        [TABLE_MENUS_LUNCH]
        [TABLE_MENUS_DINNER]
        [TABLE_MENUS_DESSERTS]
        [ICON_SHOPPING_PATH] #to be replaced within GUI class
        [INGREDIENTS]
        [OPTIONS]
        [ICON_TABLE_PATH] #to be replaced within GUI class
        '''
        
        from_day_str = menu.full_date_to_french(my_menu.start_day)
        # to_day = my_menu.start_day + timedelta(days = my_menu.number_of_days - 1)
        to_day = my_menu.to_day()
        to_day_str = menu.full_date_to_french(to_day)
        TITLE = 'du %s au %s' % (from_day_str, to_day_str)
        subject = 'Nouveaux menus (%s-%s)' % (my_menu.start_day.strftime('%d/%m/%Y'), to_day.strftime('%d/%m/%Y'))

        table_days = '<td style="width: 12.5%; text-align: center;"><span style="color: #1a5d75;"><strong>[DAY]</strong></span></td>'
        table_menus = '<td style="width: 12.5%; text-align: center;"><span style="color: #36a9d3;">[MENU]</span></td>'
        
        TABLE_DAYS = ''
        TABLE_MENUS_LUNCH = ''
        TABLE_MENUS_DINNER = ''
        # TABLE_MENUS_DESSERTS = ''

        for col in my_menu.full_menu():
            day_str, lunch_recipe, dinner_recipe = col
            
            if type(lunch_recipe) == Recipe:
                recipe_lunch_stack = [lunch_recipe]
            elif type(lunch_recipe) == list:
                recipe_lunch_stack = lunch_recipe
            
            if type(dinner_recipe) == Recipe:
                recipe_dinner_stack = [dinner_recipe]
            elif type(dinner_recipe) == list:
                recipe_dinner_stack = dinner_recipe
            
            
            lunch_str = ' | '.join(lunch_recipe.name for lunch_recipe in recipe_lunch_stack)
            dinner_str = ' | '.join(dinner_recipe.name for dinner_recipe in recipe_dinner_stack)

            TABLE_DAYS += table_days.replace('[DAY]', day_str)
            TABLE_MENUS_LUNCH += table_menus.replace('[MENU]', lunch_str)
            TABLE_MENUS_DINNER += table_menus.replace('[MENU]', dinner_str)
        
        # for dessert in my_menu.desserts:
        #     dessert_str = dessert.name

        #     TABLE_MENUS_DESSERTS += table_menus.replace('[MENU]', dessert_str)

        ingredients = '<li>[ING]</li>'
        table_style = '<table style="background: #ffcb77;" width="450" cellspacing="0" cellpadding="4" bgcolor="#ffcb77">\
            <tbody><tr style="background: transparent;"><td style="border: 1.30pt solid #36a9d3; padding: 0.1cm;" valign="top" width="470">'
        table_style_ = '</td></tr></tbody></table>'
        options_html = '<li>[ING]</li>'

        INGREDIENTS = ''
        OPTIONS = ''

        options = []
        missing = []
        
        for ingredient, qty_unit in my_menu.get_shopping_list().items():
            if ingredient != 'missing information':
                string = ''
                string_option = ''
                qty, unit = qty_unit
                if ingredient[0] == '[' and ingredient[-1] == ']':
                    string_option += '%s : %s' % (ingredient, qty)
                    if unit != '()':
                        string_option += unit
                    options.append(string_option)
                else:
                    string += '%s : %s' % (ingredient, qty)
                    if unit != '()':
                        string += unit
                    INGREDIENTS += ingredients.replace('[ING]', string)
            else:
                missing.append(qty_unit) #in that case qty_unit is recipe name
        
        if len(options) > 0:
            OPTIONS += '<p><span style="color: #36a9d3; font-size: large;"><strong>Optionnel :</strong></span></p>%s<ul>' % table_style
            for option in options:
                OPTIONS += options_html.replace('[ING]', option)
            OPTIONS += '</ul>' + table_style_
        
        if len(missing) > 0:
            OPTIONS += '<p><span style="color: #36a9d3; font-size: large;"><strong>\
                Ingr&eacute;dients manquants pour :</strong></span></p>%s<ul>' % table_style
            for recipe_name in missing[0]:
                OPTIONS += options_html.replace('[ING]', recipe_name)
            OPTIONS += '</ul>%s<p>&nbsp;</p>' % table_style_
        
        with open(self.CORE_SHOPPING_HTML, 'r') as f:
            data = f.readlines()
        
        core_text = ''.join(map(str.strip, data))

        rep = {'[TITLE]': TITLE} #define desired replacements here
        rep['[TABLE_DAYS]'] = TABLE_DAYS
        rep['[TABLE_MENUS_LUNCH]'] = TABLE_MENUS_LUNCH
        rep['[TABLE_MENUS_DINNER]'] = TABLE_MENUS_DINNER
        # rep['[TABLE_MENUS_DESSERTS]'] = TABLE_MENUS_DESSERTS
        rep['[INGREDIENTS]'] = INGREDIENTS
        rep['[OPTIONS]'] = OPTIONS
        
        text = replace_multiple(core_text, rep)
        html_body = replace_multiple(text, images_dict)
        
        self.send(to_email, subject, html_body, files = images)
    
    def send(self, to_email, subject, body, files = None):
        debug = True
        try:
            creds = get_credentials(debug=debug)
            service = build_gmail_service(creds, debug=debug)
            
            message = build_message(self.sender, 
                            to_email, 
                            subject, 
                            body,
                            files)
            message = insert_message(service, to_email, message)
            
            # send_mail_with_attachment(self.sender, to_email, subject, body, files)
            # print('Message %s sent to %s' % (subject, to_email))
            self.on_message.emit('Message "%s" envoyé à %s' % (subject, to_email), self.icon_path)
        except:
            if self.occurences < 2: 
                print('Request failed, trying to regenerate token with authorization process...')
                #delete token.json and run again
                if os.path.exists('token.json'):
                    os.remove('token.json')
                #increment occurences
                self.occurences += 1
                self.run()
            else:
                print(sys.exc_info())
                self.on_message.emit("Erreur lors de l'envoi du message '%s' à %s" % (subject, to_email), "")
            

if __name__ == '__main__':
    # add_event_standalone(title='Hello', description='tout va bien', start= datetime.datetime(2021,9,10,11))
    # try:
    #     creds = get_credentials(debug=True)
    #     # service = build_calendar_service(creds, debug=True)
    #     # timeZone = getTimeZone(service, debug=True)
    #     # id = createCalendar(service, timeZone, debug=True)
        
    #     service = build_gmail_service(creds, debug=True)
    #     # message = build_message('notification.a.table@gmail.com', 
    #     #                         'varlet.ju@gmail.com', 
    #     #                         'hello', 
    #     #                         'world')
        
    #     # message = create_message_with_attachment('notification.a.table@gmail.com', 
    #     #                         'varlet.ju@gmail.com', 
    #     #                         'hello', 
    #     #                         'world', 
    #     #                         '/home/jv/Documents/gitRepos/a_table/diagram.svg')
    #     message = create_message('notification.a.table@gmail.com', 
    #                             'varlet.ju@gmail.com', 
    #                             'hello', 
    #                             'world')
    #     insert_message(service, 'varlet.ju@gmail.com', message)
    # except:
    #     print("Unexpected error:", sys.exc_info())
        
    # creds = get_credentials(debug=True)
    # service = build_gmail_service(creds, debug=True)
    
    # message = create_message('notification.a.table@gmail.com', 
    #                             'varlet.ju@gmail.com', 
    #                             'hello', 
    #                             'world')
    # message = create_message_with_attachment('notification.a.table@gmail.com', 
    #                         'varlet.ju@gmail.com', 
    #                         'hello', 
    #                         'world', 
    #                         '/home/jv/Documents/gitRepos/a_table/diagram.svg')
    
    # message = build_message('notification.a.table@gmail.com', 
    #                         'varlet.ju@gmail.com', 
    #                         'hello', 
    #                         'world')
    # message = insert_message(service, 'varlet.ju@gmail.com', message)
    # print(message)
    
    print(is_internet_available())