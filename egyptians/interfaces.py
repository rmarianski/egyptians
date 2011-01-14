from zope.interface import Attribute
from zope.interface import Interface

class IUser(Interface):
    """represents a user

    contains nothing more than an identifier. maybe this isn't necessary then"""
    id = Attribute("user id")

class IUserFolder(Interface):
    """a container for users"""

    def add(user):
        """add a user"""

    def remove(user):
        """remove a user"""

    def list():
        """return a sequence of users"""

    def get(userid):
        """return the user specified by the id"""

class IUserInfo(Interface):
    """provides some common user metadata"""

    id = Attribute("id of user. redundant with user object, "
                   "although can be convenient")
    name = Attribute("user name")
    email = Attribute("user email address")


class IUserAuth(Interface):
    """authentication api"""

    def extract_credentials():
        """return the credentials or password from user object"""

    def authenticate(password):
        """returns true if password matches"""


class IPasswordHasher(Interface):
    """handles password hashing"""

    def hash(cleartext):
        """returns the hash of a cleartext password"""

    scheme = Attribute("string identifier of the password hashing scheme")
