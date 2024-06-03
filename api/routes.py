from app.users.handler import UserHandler
from app.messages.handler import MessageHandler


class Routes:
    def __init__(self):
        self.route_list = ['/users', '/messages']
    
    def map_routes(self, path, method, body={}, query_params={}):        
        self.user_handler = UserHandler(body=body, query_params=query_params)
        self.message_handler = MessageHandler(body=body, query_params=query_params)

        routes = {
            '/users/GET': self.user_handler.get,
            '/users/POST': self.user_handler.create,
            '/users/PUT': self.user_handler.update,
            '/users/DELETE': self.user_handler.delete,
            '/messages/GET': self.message_handler.get,
            '/messages/POST': self.message_handler.create,
            '/messages/PUT': self.message_handler.update,
            '/messages/DELETE': self.message_handler.delete,
        }

        key = f'{path}/{method}'

        route = routes.get(key)
        return route()
    