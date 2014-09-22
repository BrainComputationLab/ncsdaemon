""" module for user management stuff """
from ncsdaemon.crypt import Crypt
from ncsdaemon.database import Database
import ipaddress


class UserManager(object):
    """ Class that handles users """

    def __init__(self):
        self.db = Database()

    def create_user(self, username, first_name, last_name, email, institution,
                    password):
        # check for existing users with that username
        users = list(Database.User.find({'username': username}))
        # if there are raise an exception
        if len(users):
            raise Exception("User already exists")
        # generate a new cryptographic salt
        salt = Crypt.generate_salt()
        # create the new user
        new_user = Database.User({
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'institution': institution,
            'password': Crypt.hash_password(password, salt),
            'salt': salt
        })
        # save the new user
        new_user.save()

    def verify_user(self, username, password):
        user = Database.User.one({'username': username})
        if not user:
            raise Exception("User does not exist")
        hash_pass = Crypt.hash_password(password, user.salt)
        return True if hash_pass == user.password else False

    def validate_token(self, username, token, ip):
        u = Database.User.one({'username': username, 'token': token, 'ip': ip})
        return True if u else False

    def get_user_by_username(self, username):
        return Database.User.one({'username': username})
