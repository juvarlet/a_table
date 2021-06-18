"""
Adapted from:
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
https://developers.google.com/identity/protocols/OAuth2

1. Generate and authorize an OAuth2 (generate_oauth2_token)
2. Generate a new access tokens using a refresh token(refresh_token)
3. Generate an OAuth2 string to use for login (access_token)
"""

import base64
import imaplib
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PySide2.QtCore import QThread
import lxml.html
from os.path import basename
from email.mime.application import MIMEApplication

from email.mime.image import MIMEImage

import menu
import re
import os

from PySide2.QtGui import *
from PySide2.QtCore import *

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

GOOGLE_CLIENT_ID = '1088222992614-4vsa7ucaf35tlscpdus03vqk3ephkc2b.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'tTAnmKKftItOcjcj3W-4tuy1'
# GOOGLE_REFRESH_TOKEN = '1//0djMyilP7FTEiCgYIARAAGA0SNwF-L9IrtWefq53LohFyS2OUCznalVS8EJAwLtfhiPKw-yw-9NEeG1z0mNKZDy6JlCQTw1NUCPg'

def read_token():
    token_file = os.path.dirname(__file__) + '/token.id'
    with open(token_file, 'r') as f:
        token = f.readlines()[0].rstrip()
    return token
GOOGLE_REFRESH_TOKEN = read_token()

APP_MAIL = 'notification.a.table@gmail.com'
PASSWORD = '@table_@dmin'
FULL_NAME = "Maitre D'hotel"

CORE_SHOPPING_HTML = os.path.dirname(__file__) + '/shopping_core.html'
CORE_RECIPE_HTML = os.path.dirname(__file__) + '/recipe_core.html'

def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)


def url_escape(text):
    return urllib.parse.quote(text, safe='~-._')


def url_unescape(text):
    return urllib.parse.unquote(text)


def url_format_params(params):
    param_fragments = []
    for param in sorted(params.items(), key=lambda x: x[0]):
        param_fragments.append('%s=%s' % (param[0], url_escape(param[1])))
    return '&'.join(param_fragments)


def generate_permission_url(client_id, scope='https://mail.google.com/'):
    params = {}
    params['client_id'] = client_id
    params['redirect_uri'] = REDIRECT_URI
    params['scope'] = scope
    params['response_type'] = 'code'
    return '%s?%s' % (command_to_url('o/oauth2/auth'), url_format_params(params))


def call_authorize_tokens(client_id, client_secret, authorization_code):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['code'] = authorization_code
    params['redirect_uri'] = REDIRECT_URI
    params['grant_type'] = 'authorization_code'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def call_refresh_token(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string


def test_imap(user, auth_string):
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')


def test_smpt(user, base64_auth_string):
    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(True)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64_auth_string)


def get_authorization(google_client_id, google_client_secret):
    scope = "https://mail.google.com/"
    print('Navigate to the following URL to auth:', generate_permission_url(google_client_id, scope))
    authorization_code = input('Enter verification code: ')
    response = call_authorize_tokens(google_client_id, google_client_secret, authorization_code)
    return response['refresh_token'], response['access_token'], response['expires_in']


def refresh_authorization(google_client_id, google_client_secret, refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, refresh_token)
    return response['access_token'], response['expires_in']


def send_mail(fromaddr, toaddr, subject, message):
    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)
    # print(expires_in)

    msg = MIMEMultipart('related')
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
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

def send_mail_with_attachment(fromaddr, toaddr, subject, message, files = None):
    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)
    # print(expires_in)

    msg = MIMEMultipart('related')
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

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

class MySignal(QObject):
    sig = Signal(str)

class Mailbox(QThread):#QThread
    # def __init__(self, my_menu, to_email, images, images_dict):#, my_menu, to_email, images, images_dict
    def __init__(self, option, list_args):
        QThread.__init__(self)#<-
        if GOOGLE_REFRESH_TOKEN is None:
            print('No refresh token found, obtaining one')
            refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
            print('Set the following as your GOOGLE_REFRESH_TOKEN:', refresh_token)
            exit()
        
        self.sender = 'notification.a.table@gmail.com'
        
        self.option = option
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
            
        self.signal = MySignal()
        
    def run(self):#<-
        if self.option == 'shopping':
            # self.signal.sig.emit('starting...')
            self.send_shopping_list(self.my_menu, self.to_email, self.images, self.images_dict)#<-
            # self.signal.sig.emit('complete')
        elif self.option == 'recipe':
            self.send_recipe(self.recipe, self.to_email, self.images, self.images_dict, self.pdf)
    
    def send(self, to_email, subject, body, files = None):
        try:
            send_mail_with_attachment(self.sender, to_email, subject, body, files)
            # print('Message %s sent to %s' % (subject, to_email))
            self.signal.sig.emit('Message "%s" envoyé à %s' % (subject, to_email))
        except:
            self.signal.sig.emit("Votre autorisation pour l'envoi de messages a probablement expiré, vous pouvez demander une mise à jour à %s" 
                                 % self.sender)

    def send_recipe(self, recipe, to_email, images, images_dict, pdf):
        # print('send recette')
        TITLE = recipe.name
        subject = 'Fiche recette - %s' % recipe.name

        with open(CORE_RECIPE_HTML, 'r') as f:
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

        table_days = '<td style="width: 12.5%; text-align: center;"><span style="color: #5c3c92;"><strong>[DAY]</strong></span></td>'
        table_menus = '<td style="width: 12.5%; text-align: center;"><span style="color: #077b8a;">[MENU]</span></td>'
        
        TABLE_DAYS = ''
        TABLE_MENUS_LUNCH = ''
        TABLE_MENUS_DINNER = ''
        TABLE_MENUS_DESSERTS = ''

        for col in my_menu.full_menu():
            day_str, lunch_recipe, dinner_recipe = col
            lunch_str = lunch_recipe.name
            dinner_str = dinner_recipe.name

            TABLE_DAYS += table_days.replace('[DAY]', day_str)
            TABLE_MENUS_LUNCH += table_menus.replace('[MENU]', lunch_str)
            TABLE_MENUS_DINNER += table_menus.replace('[MENU]', dinner_str)
        
        for dessert in my_menu.desserts:
            dessert_str = dessert.name

            TABLE_MENUS_DESSERTS += table_menus.replace('[MENU]', dessert_str)

        ingredients = '<li>[ING]</li>'
        table_style = '<table style="background: #a2d5c6;" width="450" cellspacing="0" cellpadding="4" bgcolor="#a2d5c6">\
            <tbody><tr style="background: transparent;"><td style="border: 1.30pt solid #077b8a; padding: 0.1cm;" valign="top" width="470">'
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
            OPTIONS += '<p><span style="color: #077b8a; font-size: large;"><strong>Optionnel :</strong></span></p>%s<ul>' % table_style
            for option in options:
                OPTIONS += options_html.replace('[ING]', option)
            OPTIONS += '</ul>' + table_style_
        
        if len(missing) > 0:
            OPTIONS += '<p><span style="color: #077b8a; font-size: large;"><strong>\
                Ingr&eacute;dients manquants pour :</strong></span></p>%s<ul>' % table_style
            for recipe_name in missing[0]:
                OPTIONS += options_html.replace('[ING]', recipe_name)
            OPTIONS += '</ul>%s<p>&nbsp;</p>' % table_style_
        
        with open(CORE_SHOPPING_HTML, 'r') as f:
            data = f.readlines()
        
        core_text = ''.join(map(str.strip, data))

        rep = {'[TITLE]': TITLE} #define desired replacements here
        rep['[TABLE_DAYS]'] = TABLE_DAYS
        rep['[TABLE_MENUS_LUNCH]'] = TABLE_MENUS_LUNCH
        rep['[TABLE_MENUS_DINNER]'] = TABLE_MENUS_DINNER
        rep['[TABLE_MENUS_DESSERTS]'] = TABLE_MENUS_DESSERTS
        rep['[INGREDIENTS]'] = INGREDIENTS
        rep['[OPTIONS]'] = OPTIONS
        
        text = replace_multiple(core_text, rep)
        html_body = replace_multiple(text, images_dict)
        
        self.send(to_email, subject, html_body, files = images)
    

def replace_multiple(string, from_to_dict):
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in from_to_dict.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
    return text


        
    
def debug():
    my_mailbox = Mailbox()
    my_mailbox.send('varlet.ju@gmail.com', 'hello', 'bonjour Julien')

if __name__ == '__main__':
    # debug()
    refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    print('Set the following as your GOOGLE_REFRESH_TOKEN:', refresh_token)
    exit()