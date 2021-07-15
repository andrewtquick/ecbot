import os
import firebase_admin
from misc.utils import Utils
from discord import Member as Member
from discord import Guild as Guild
from firebase_admin import credentials, db

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
    'databaseURL': os.getenv('DB_URL') 
})

class DBConnection():

    def __init__(self):
        self.utils = Utils(self)
        self.ecdb = db.reference()

    # Checking if user exists in db

    def check_user(self, guild, member):
        get_user = self.ecdb.child(str(guild.id))
        get_data = get_user.get()

        if 'users' in get_data:
            if str(member.id) in get_data['users']:
                return True
            else:
                return False
        else:
            return False

    # Getting date member joined server

    def get_date(self, guild, member):
        user_join = self.ecdb.child(str(guild.id)).child('users')
        get_join_date = user_join.get()
        return get_join_date[str(member.id)]['joined_at']

    # Adding new user to db

    def add_new_user(self, guild: str, member: str):
        new_user = self.ecdb.child(str(guild.id)).child('users')
        parsed_date = self.utils.parse_date_time(str(member.joined_at))
        member_roles = [role.name for role in member.roles]
        new_user.update({
            str(member.id): {
                'member': str(member),
                'member_id': str(member.id),
                'member_name': str(member.name),
                'display_name': str(member.display_name),
                'joined_at': parsed_date,
                'roles': member_roles
            }})

    # Checking if guild exists

    def check_guild(self, guild: str):
        get_guild = self.ecdb.child(str(guild))
        get_data = get_guild.get()

        if get_data == None:
            return False
        else:
            return True
