import time

class Utils(object):

    def __init__(self, object):
        self.utils = object
        
    # Parsing Date and Time to readable format

    def parse_date_time(self, date_time):

        entry = str(date_time)
        parsed_entry = time.strptime(entry.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parsed_entry = time.strftime('%m-%d-%Y %I:%M %p', parsed_entry)

        return parsed_entry