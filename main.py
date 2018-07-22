"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""
from app.api.app import init_app
from wsgiref import simple_server

app = init_app()

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
