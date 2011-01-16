from zope.interface import implements
from egyptians.interfaces import IUserAuth

import hashlib

class UserAuth(object):
    implements(IUserAuth)

    def __init__(self, context):
        self.context = context

    def _get_password(self):
        return self.context.password
    def _set_password(self, password):
        self.context.password = password
    password = property(_get_password, _set_password)
