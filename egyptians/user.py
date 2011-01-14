from persistent import Persistent
from repoze.folder import Folder
from zope.interface import implements
from egyptians.interfaces import IUser
from egyptians.interfaces import IUserFolder
from egyptians.interfaces import IUserInfo

class User(Persistent):
    implements(IUser)

    name = u''
    email = u''
    password = u''

    def __init__(self, id, **kwargs):
        self.id = id
        self.__dict__.update(kwargs)

class UserFolder(Folder):
    implements(IUserFolder)

    def add(self, user):
        self[user.id] = user

    def remove(self, user):
        del self[user.id]

    def list(self):
        return self.keys()

    def get(self, id):
        return self[id]

class UserInfo(object):
    """simple adapter implementation

    delegates to actual user object for info"""

    implements(IUserInfo)

    def __init__(self, context):
        self.context = context

    @property
    def id(self):
        return self.context.id

    def _get_name(self):
        return self.context.name
    def _set_name(self, name):
        self.context.name = name
    name = property(_get_name, _set_name)

    def _get_email(self):
        return self.context.email
    def _set_email(self, email):
        self.context.email = email
    email = property(_get_email, _set_email)
