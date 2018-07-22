import falcon

from app.utils.tokens import read_token


def validate_token(req, resp, resource, params):
    try:
        if req.auth == "":
            raise Exception("Debes enviar un token de acceso en la cabecera Authorization.")
        token = req.auth.replace('Bearer ', '')
        req.context['user'] = read_token(token)
        print(req.context['user'])
        token_type = req.context['user'].get('type', '')
        if token_type != 'access_token':
            raise Exception("El token no es válido. Puede haber caducado.")
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('The provided auth token is not valid. '
                       'Please request a new token and try again.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')