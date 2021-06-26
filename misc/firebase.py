import os
import firebase_admin
from misc.utils import Utils
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate({
    "type": os.getenv('GCP_TOKEN_TYPE'),
    "project_id": os.getenv('GCP_TOKEN_PROJECT_ID'),
    "private_key_id": os.getenv('GCP_TOKEN_PRIVATE_KEY_ID'),
    "private_key": os.getenv('GCP_TOKEN_PRIVATE_KEY').replace(r'\n', '\n'),
    "client_email": os.getenv('GCP_TOKEN_CLIENT_EMAIL'),
    "client_id": os.getenv('GCP_TOKEN_CLIENT_ID'),
    "auth_uri": os.getenv('GCP_TOKEN_AUTH_URI'),
    "token_uri": os.getenv('GCP_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('GCP_TOKEN_AUTH_PROVIDER'),
    "client_x509_cert_url": os.getenv('GCP_TOKEN_CLIENT_CERT')
    })

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ecbot-data-storage-default-rtdb.firebaseio.com/' 
})

class DBConnection(object):

    def __init__(self, object):
        self.db = object
        self.utils = Utils(self)

        self.ecdb = db.reference()

    def check_user(self, member_id):
        user_list = self.ecdb.get()

        if member_id in user_list['users']:
            return True
        else:
            return False


    def get_date(self, member_id):
        get_join_date = self.ecdb.get()

        return get_join_date['users'][member_id]['joined_at']

    def add_new_user(self, member_id, member, member_name, joined_at):
        new_user = self.ecdb.child('users')
        parsed_date = self.utils.parse_date_time(str(joined_at))
        new_user.update({
            str(member_id): {
                'member': str(member),
                'member_name': str(member_name),
                'joined_at': parsed_date
            }})
