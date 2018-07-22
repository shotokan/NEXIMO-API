import time
import uuid

from datetime import datetime


def response_ok(body, status, msg, method, path, version='v1'):
    now = datetime.now()

    epoch = time.mktime(now.timetuple())
    data = {
            'response_id': str(uuid.uuid4()),
            'path': path,
            'method': method,
            'request': epoch,
            'msg': msg,
            'api-version': version,
            'status': status,
            'service': 'NEXIMO-API',
            'data': body,
        }
    print(data)
    return data


def response_error(body, msg, method, path, version='v1'):
    now = datetime.now()

    epoch = time.mktime(now.timetuple())
    if isinstance(body, str):
        body = {
            'error': body
        }
    return {
            'path': path,
            'method': method,
            'request': epoch,
            'api-version': version,
            'msg': msg,
            'service': 'NEXIMO-API',
            'data': body,
        }