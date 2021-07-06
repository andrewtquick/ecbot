import time
import pytz
import requests
import os
from datetime import datetime as dt

class Utils(object):

    def __init__(self, object):
        self.utils = object
        self.CLIENT_ID = os.getenv('WOW_API')
        self.CLIENT_SECRET = os.getenv('API_SECRET')
        self.tz = pytz.timezone('America/New_York')
        
    # Parsing Input to readable format

    def parse_date_time(self, date_time):
        entry = str(date_time)
        parsed_entry = time.strptime(entry.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parsed_entry = time.strftime('%m-%d-%Y %I:%M %p', parsed_entry)
        return parsed_entry

    # Getting date and time and parsing for output

    def get_date_time_parsed(self):
        now = str(dt.now(self.tz))
        parse_now = time.strptime(now.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parse_now = time.strftime('%m-%d-%Y %I:%M %p', parse_now)
        return parse_now

    def get_time_parsed(self):
        now = str(dt.now(self.tz))
        parse_now = time.strptime(now.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parse_now = time.strftime('%I:%M %p', parse_now)
        return parse_now

    def blizzard_access_token(self):
        data = { 'grant_type' : 'client_credentials' }
        resp = requests.post('https://us.battle.net/oauth/token', data=data, auth=(self.CLIENT_ID, self.CLIENT_SECRET)).json()
        return resp['access_token']

    def channel_parse(self, chan: str):

        try:
            int(chan)
            return True
        except ValueError:
            return False