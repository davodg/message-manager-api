from api.request_handler import RequestHandler
import json

def url_handlers(environ, start_reponse):
    request_handler = RequestHandler(environ)

    data, status = request_handler.handle_request()

    data = data.encode('utf-8')
    content_type = 'application/json' if int(status.split(' ')[0]) < 400 else 'text/plain'
    response_headers = [('Content-Type', content_type), ('Content-Length', str(len(data)))]

    start_reponse(status, response_headers)
    return data
