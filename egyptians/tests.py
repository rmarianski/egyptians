import unittest

from pyramid.config import Configurator
from pyramid import testing

class UserTests(unittest.TestCase):

    def _getTargetClass(self):
        from egyptians.user import User
        return User

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_create_user(self):
        user = self._makeOne(u'marty')
        self.assertEquals(u'marty', user.id)

    def test_user_implements_interface(self):
        from zope.interface.verify import verifyObject
        from egyptians.interfaces import IUser
        user = self._makeOne(u'mcfly')
        verifyObject(IUser, user)


class UserFolderTests(unittest.TestCase):

    def _getTargetClass(self):
        from egyptians.user import UserFolder
        return UserFolder

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeUser(self, *args, **kw):
        from egyptians.user import User
        return User(*args, **kw)

    def test_userfolder_implements_interface(self):
        from zope.interface.verify import verifyObject
        from egyptians.interfaces import IUserFolder
        userfolder = self._makeOne()
        verifyObject(IUserFolder, userfolder)


class UserInfoTests(unittest.TestCase):

    def _getTargetClass(self):
        from egyptians.user import UserInfo
        return UserInfo

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeUser(self):
        from egyptians.user import User
        user = User(u'biff')
        return user

    def test_userinfo_implements_interface(self):
        from zope.interface.verify import verifyObject
        from egyptians.interfaces import IUserInfo
        user = self._makeUser()
        userinfo = self._makeOne(user)
        verifyObject(IUserInfo, userinfo)

    def test_userinfo_readproperties_set(self):
        user = self._makeUser()
        userinfo = self._makeOne(user)
        userinfo.name = u'Biff Tannen'
        userinfo.email = u'biff@example.com'
        self.assertEquals(u'biff', userinfo.id)
        self.assertEquals(u'Biff Tannen', userinfo.name)
        self.assertEquals(u'biff@example.com', userinfo.email)

    def test_userinfo_readproperties_notset(self):
        user = self._makeUser()
        userinfo = self._makeOne(user)
        self.assertEquals(u'biff', userinfo.id)
        self.assertEquals(u'', userinfo.name)
        self.assertEquals(u'', userinfo.email)

    def test_userinfo_writeproperties(self):
        user = self._makeUser()
        userinfo = self._makeOne(user)
        userinfo.name = u'Marty McFly'
        userinfo.email = u'marty@example.com'
        self.assertEquals(u'biff', userinfo.id)
        self.assertEquals(u'Marty McFly', userinfo.name)
        self.assertEquals(u'marty@example.com', userinfo.email)


class UserAuthTests(unittest.TestCase):

    def _getTargetClass(self):
        from egyptians.auth import UserAuth
        return UserAuth

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeUser(self):
        from egyptians.user import User
        user = User(u'emmett-brown')
        user.password = u'flux capacitor'
        return user

    def test_userauth_implements_interface(self):
        from zope.interface.verify import verifyObject
        from egyptians.interfaces import IUserAuth
        user = self._makeUser()
        userauth = self._makeOne(user)
        verifyObject(IUserAuth, userauth)

    def test_userauth_extract_credentials(self):
        user = self._makeUser()
        userauth = self._makeOne(user)
        self.assertEquals(u'flux capacitor', userauth.extract_credentials())

    def test_userauth_update_credentials(self):
        user = self._makeUser()
        userauth = self._makeOne(user)
        userauth.update_credentials(u'delorean')
        self.assertEquals(u'delorean', userauth.extract_credentials())

    def test_userauth_authenticate(self):
        user = self._makeUser()
        userauth = self._makeOne(user)
        self.failUnless(userauth.authenticate(u'flux capacitor'))


class PasswordHasherTests(unittest.TestCase):

    def _getTargetClass(self):
        from egyptians.auth import PasswordHasher
        return PasswordHasher

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_hasher_implements_interface(self):
        from egyptians.interfaces import IPasswordHasher
        from zope.interface.verify import verifyObject
        hasher = self._makeOne()
        verifyObject(IPasswordHasher, hasher)

    def test_hash(self):
        hasher = self._makeOne()
        hash = hasher.hash(u'flux capacitor')
        self.assertEquals(
            '9fc09459ed54aa1a6019fa1eb9d3234cc4dcb50ff8cd32a8c233d334',
            hash)

    def test_scheme(self):
        hasher = self._makeOne()
        self.assertEquals('sha224', hasher.scheme)
