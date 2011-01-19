import colander
import deform

from egyptians.interfaces import IUserAuth
from egyptians.interfaces import IUserGroups
from interfaces import IUserInfo
from pyramid.security import forget
from pyramid.security import remember
from pyramid.url import resource_url
from user import User
from utils import make_slug
from webob.exc import HTTPFound
from zope.password.interfaces import IPasswordManager

class LoginSchema(colander.Schema):
    login = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String(),
                                   widget=deform.widget.PasswordWidget())

def check_password_validator(context, registry):
    def check_password(node, value):
        user_id = value['login']
        try:
            user = context.get_user(user_id)
        except KeyError:
            exc = colander.Invalid(node, u'Unknown user')
            exc['login'] = u'Unknown user'
            raise exc
        password = value['password']
        password_manager = registry.getUtility(IPasswordManager)
        user_auth = registry.getAdapter(user, IUserAuth)
        ok = password_manager.checkPassword(user_auth.password,
                                            password)
        if not ok:
            exc = colander.Invalid(node, u'Bad password')
            exc['password'] = u'Bad password'
            raise exc
    return check_password

def login_view(context, request):
    validator = check_password_validator(context, request.registry)
    schema = LoginSchema(validator=validator)
    login_form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = login_form.validate(controls)
        except deform.ValidationFailure, e:
            return {'form': e.render()}

        principal = appstruct['login']
        headers = remember(request, principal)
        return HTTPFound(location='/',
                         headers=headers,
                         )

    return {'form': login_form.render()}

def logout_view(context, request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)

class UserSchema(colander.Schema):
    username = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String(), missing=u'')
    email = colander.SchemaNode(colander.String())

def register_view(context, request):
    schema = UserSchema()
    form = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e.render())

        slug = make_slug(appstruct['username'])
        user = User(slug)
        userinfo = request.registry.getAdapter(user, IUserInfo)
        userinfo.name = appstruct['name']
        userinfo.email = appstruct['email']
        context[slug] = user
        return HTTPFound(location=resource_url(user, request))

    return dict(form=form.render())

def user_view(context, request):
    schema = UserSchema()
    form = deform.Form(schema, buttons=('submit',))
    userinfo = request.registry.getAdapter(context, IUserInfo)
    return dict(form=form.render(
            dict(username=context.id,
                 name=userinfo.name,
                 email=userinfo.email,
                 ),
            readonly=True))

class Group(colander.Schema):
    group_name = colander.SchemaNode(colander.String())

class Groups(colander.SequenceSchema):
    group = Group()

class GroupSchema(colander.Schema):
    groups = Groups()

def manage_groups_view(context, request):
    schema = GroupSchema()
    form = deform.Form(schema, buttons=('submit',))
    usergroup_manager = request.registry.getAdapter(context, IUserGroups)
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e.render())

        new_groups = [x['group_name'] for x in appstruct['groups']]
        from persistent.list import PersistentList
        usergroup_manager.groups = PersistentList(new_groups)
        return HTTPFound(location=request.url)

    existing_groups = dict(
        groups=[dict(group_name=x) for x in usergroup_manager.groups])

    return dict(form=form.render(existing_groups))

def users_view(context, request):
    reg = request.registry
    def make_user_data(user):
        userinfo = reg.getAdapter(user, IUserInfo)
        return dict(id=user.id,
                    name=userinfo.name or user.id,
                    url=resource_url(user, request),
                    )
    users_data = [make_user_data(x) for x in context.values()]
    return dict(users_data=users_data)
