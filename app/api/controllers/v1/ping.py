from app.utils.api_response import response_ok


class Ping:

    def on_get(self, req, resp):
        resp.context['result'] = response_ok({'response': 'pong'}, "ok", 'pong', 'get', req.path)
