from persistent import Persistent
from persistent.list import PersistentList
from repoze.folder import Folder
from zope.interface import implements
from egyptians.interfaces import IUser
from egyptians.interfaces import IUserFolder
from egyptians.interfaces import IUserGroups
from egyptians.interfaces import IUserInfo

class User(Persistent):
    implements(IUser)

    def __init__(self, id):
        self.id = id

class UserFolder(Folder):
    implements(IUserFolder)

    def add_user(self, user):
        self[user.id] = user

    def remove_user(self, user):
        del self[user.id]

    @property
    def userids(self):
        return self.keys()

    @property
    def users(self):
        return self.values()

    def get_user(self, id):
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
        return getattr(self.context, 'name', u'')
    def _set_name(self, name):
        self.context.name = name
    name = property(_get_name, _set_name)

    def _get_email(self):
        return getattr(self.context, 'email', u'')
    def _set_email(self, email):
        self.context.email = email
    email = property(_get_email, _set_email)


class UserGroups(object):
    """adapter to manage a user's groups"""

    implements(IUserGroups)

    def __init__(self, context):
        self.context = context

    def _get_groups(self):
        return getattr(self.context, 'groups', [])
    def _set_groups(self, groups):
        self.context.groups = groups
    groups = property(_get_groups, _set_groups)

    def add_group(self, group):
        if getattr(self.context, 'groups', None) is None:
            self.context.groups = PersistentList()
        self.context.groups.append(group)

    def remove_group(self, group):
        self.context.groups.remove(group)
