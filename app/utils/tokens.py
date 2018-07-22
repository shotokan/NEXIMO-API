import time
import jwt

from datetime import datetime, timedelta


def _open_priv_key():
    try:
        # ROOT_DIR = os.path.dirname()
        with open('./ssl/' + 'privkey.pem') as f:
            return f.read()
    except Exception as exc:
        print(exc)
        return None


def _open_pub_key():
    try:
        # ROOT_DIR = os.path.dirname()
        with open('./ssl/' + 'pubkey.pem') as f:
            return f.read()
    except Exception as exc:
        print(exc)
        return None


PRIVKEY = _open_priv_key()
PUBKEY = _open_pub_key()


def create_token(data):
    PRIVKEY = _open_priv_key()
    return jwt.encode(data, PRIVKEY, algorithm='RS512')


def read_token(token):
    return jwt.decode(token, PUBKEY, audience='neximo', verify=False, algorithms=['RS512'])


def get_data_for_access_token(data, minutes=15):
    return {
        'user_id': data['user_id'],
        'role': data['role_id'],
        'role_name': data['role_name'],
        'exp': data['access_token_expires_at'],
        'iat': data['issued_at'],
        'aud': 'neximo',
        'iss': '',
        'type': 'access_token'
    }


def get_data_for_refresh_token(data, days=2):
    return {
        'user_id': data['user_id'],
        'exp': data['refresh_token_expires_in'],
        'iat': data['issued_at'],
        'aud': 'neximo',
        'iss': '',
        'type': 'refresh_token'
    }
