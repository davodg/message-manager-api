import json
from api.routes import Routes
from app.models.response import Response

class RequestHandler(object):
    def __init__(self, environ):
        self.environ = environ
        self.request_body = self._get_body()
        self.query_params = self._get_query_params()
        self.method = self.environ.get('REQUEST_METHOD')
        self.path = self._get_path()
        self.routes = Routes()

    def handle_request(self):
        if self.path == '':
            return json.dumps({'message': 'Welcome to Message Manager API'}), '200 OK'
        
        if self.path not in self.routes.route_list:
            return json.dumps({'error': '404 Not Found'}), '404 Not Found'

        route = self.routes.map_routes(path=self.path, query_params=self.query_params, body=self.request_body, method=self.method)
        data, status = Response(route).get_response()

        return data, status

    def _get_path(self):
        path = self.environ.get('PATH_INFO')

        if path.endswith('/'):
            path = path[:-1]

        return path
    
    def _get_body(self):
        content_length = int(self.environ.get('CONTENT_LENGTH', 0))
        request_body = self.environ['wsgi.input'].read(content_length)
        body = json.loads(request_body.decode('utf-8')) if request_body else {}

        return body
    
    def _get_query_params(self):
        query_string = self.environ.get('QUERY_STRING')
        query_params = {}

        if query_string:
            query_params = dict(q.split('=') for q in query_string.split('&'))

        return query_params