from zope.interface import implements
from egyptians.interfaces import IPasswordHasher
from egyptians.interfaces import IUserAuth

import hashlib

class UserAuth(object):
    implements(IUserAuth)

    def __init__(self, context):
        self.context = context

    def extract_credentials(self):
        return self.context.password

    def authenticate(self, password):
        return self.extract_credentials() == password

class PasswordHasher(object):
    implements(IPasswordHasher)

    scheme = 'sha224'

    def hash(self, cleartext):
        return hashlib.sha224(cleartext).hexdigest()
