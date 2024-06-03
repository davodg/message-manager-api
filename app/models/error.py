

class Error(object):
    def __init__(self, error_message) -> None:
        self.error_message = error_message

    def get_400_error(self):
        return {
            'status': '400 Bad Request',
            'error': self.error_message
        }
    