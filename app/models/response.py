import json

class Response(object):
    def __init__(self, response):
        self.data = response.get('data')
        self.error = response.get('error')
        self.status_code = response['status']
        self.meta = response.get('meta', {})
        self.response = self._mount_response()

    def get_response(self):
        if self.error:
            return json.dumps(self.error), self.status_code

        return json.dumps(self.response), self.status_code
    
    def _mount_response(self):
        return {
            'meta': self.meta,
            'data': self.data,
        }