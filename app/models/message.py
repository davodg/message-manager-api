class MessageModel(object):
    def __init__(self, message: dict):
        self.id = message.get('id')
        self.status = message.get('status')
        self.text = message.get('text')
        self.creation_date = message.get('creation_date')
        self.update_date = message.get('update_date')
        self.error = message.get('error')

    def validate(self):
        if None in (self.text,):
            return False

        return True

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'creation_date': self.creation_date,
            'update_date': self.update_date,
            'error': self.error
        }
