import falcon
import json

from app.utils.json_serializer import json_serializer


class JSONTranslator:
    # NOTE: Starting with Falcon 1.3, you can simply
    # use req.media and resp.media for this instead.

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        print('en process requests')
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['data'] = json.loads(body.decode('utf-8'))
            if 'data' in req.context['data']:
                # if exist a data property in json, it is passes like data into context
                req.context['data'] = req.context['data']['data']

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in resp.context:
            return

        resp.body = json.dumps(resp.context['result'], default=json_serializer)
