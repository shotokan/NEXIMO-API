import falcon

from app.utils.tokens import read_token


class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        service_id = req.get_header('Service-ID')

        challenges = ['Token type="jwt"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token):
        try:
            token = token.replace("Bearer ", "")
            try:
                print(read_token(token))
                return True
            except:
                return False

        except Exception:
            return False
