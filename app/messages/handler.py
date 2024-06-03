from app.messages.repository import MessageRepository
from app.models.error import Error
from app.models.message import MessageModel

class MessageHandler:
    def __init__(self, body={}, query_params={}):
        self.repository = MessageRepository()
        self.message = MessageModel(body)
        self.query_params = query_params

    def get(self):
        message_id = self.query_params.get('message_id')
        page = int(self.query_params.get('page', 1))
        limit = int(self.query_params.get('limit', 20))

        return self.repository.get(message_id=message_id, page=page, limit=limit)

    def create(self):
        if not self.message.validate():
            return Error('Invalid message data').get_400_error()

        return self.repository.create(self.message)

    def update(self):
        message_id = self.query_params.get('message_id')

        if not message_id:
            return Error("Missing 'message_id' parameter").get_400_error()

        if not self.message.validate():
            return Error('Invalid message data').get_400_error()

        return self.repository.update(message_id, self.message)

    def delete(self):
        message_id = self.query_params.get('message_id')

        if not message_id:
            return Error("Missing 'message_id' parameter").get_400_error()
        
        return self.repository.delete(message_id)