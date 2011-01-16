from zope.interface import Attribute
from zope.interface import Interface

class IUser(Interface):
    """represents a user

    contains nothing more than an identifier. maybe this isn't necessary then"""
    id = Attribute("user id")

class IUserFolder(Interface):
    """a container for users"""

    def add_user(user):
        """add a user"""

    def remove_user(user):
        """remove a user"""

    def get_user(userid):
        """return the user specified by the id"""

    userids = Attribute("sequence of userids in folder")
    users = Attribute("sequence of user objects in folder")

class IUserInfo(Interface):
    """provides some common user metadata"""

    id = Attribute("id of user. redundant with user object, "
                   "although can be convenient")
    name = Attribute("user name")
    email = Attribute("user email address")


class IUserAuth(Interface):
    """authentication api"""

    password = Attribute("user password")

class IUserGroups(Interface):
    """management around a user's groups"""

    groups = Attribute("sequence of groups")

    def add_group(group):
        """add a new group"""

    def remove_group(group):
        """remove a group"""
