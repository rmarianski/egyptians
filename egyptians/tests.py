import unittest

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

    def test_userfolder_add(self):
        userfolder = self._makeOne()
        user = self._makeUser(u'george')
        userfolder.add_user(user)
        self.failUnless(u'george' in userfolder.keys())

    def test_userfolder_remove(self):
        userfolder = self._makeOne()
        user = self._makeUser(u'george')
        userfolder.add_user(user)
        self.failUnless(u'george' in userfolder.keys())
        userfolder.remove_user(user)
        self.failIf(u'george' in userfolder.keys())

    def test_userfolder_userids(self):
        userfolder = self._makeOne()
        user1 = self._makeUser(u'george')
        user2 = self._makeUser(u'lorraine')
        userfolder.add_user(user1)
        userfolder.add_user(user2)
        userids = userfolder.userids
        self.assertEquals(2, len(userids))
        self.assertEquals(u'george', userids[0])
        self.assertEquals(u'lorraine', userids[1])

    def test_userfolder_users(self):
        userfolder = self._makeOne()
        user1 = self._makeUser(u'george')
        user2 = self._makeUser(u'lorraine')
        userfolder.add_user(user1)
        userfolder.add_user(user2)
        users = userfolder.users
        self.assertEquals(2, len(users))
        self.assertEquals(u'george', users[0].id)
        self.assertEquals(u'lorraine', users[1].id)

    def test_userfolder_get_user(self):
        userfolder = self._makeOne()
        user = self._makeUser(u'george')
        userfolder.add_user(user)
        self.assertEquals(u'george', userfolder.get_user(u'george').id)


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

    def test_userauth_getpassword(self):
        user = self._makeUser()
        userauth = self._makeOne(user)
        self.assertEquals(u'flux capacitor', userauth.password)

    def test_userauth_setpassword(self):
        user = self._makeUser()
        userauth = self._makeOne(user)
        userauth.password = u'delorean'
        self.assertEquals(u'delorean', userauth.password)
