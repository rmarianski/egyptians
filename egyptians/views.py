import colander
import deform

from egyptians.interfaces import IUserAuth
from egyptians.interfaces import IUserGroups
from pyramid.security import forget
from pyramid.security import remember
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

class Group(colander.Schema):
    group_name = colander.SchemaNode(colander.String())

class Groups(colander.SequenceSchema):
    group = Group()

class Schema(colander.Schema):
    groups = Groups()

def manage_groups_view(context, request):
    schema = Schema()
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
