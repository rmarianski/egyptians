import colander
import deform

from egyptians.interfaces import IPasswordHasher
from egyptians.interfaces import IUserAuth
from pyramid.security import remember

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
        password_hasher = registry.getUtility(IPasswordHasher)
        user_auth = registry.getAdapter(user, IUserAuth)
        hashed_password = password_hasher.hash(password)
        if not user_auth.authenticate(hashed_password):
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
        from webob import Response
        return Response(body=u'Great success',
                        headers=headers,
                        )

    return {'form': login_form.render()}
