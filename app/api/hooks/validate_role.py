import falcon


def validate_scope_student(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "estudiante":
                raise Exception("You must be a student.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')


def validate_scope_professor(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "profesor":
                raise Exception("You must be a teacher.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')


def validate_scope_both(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "profesor" and role.lower() != "estudiante":
                raise Exception("You must be a teacher or student.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')