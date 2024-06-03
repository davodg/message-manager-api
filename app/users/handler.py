from app.users.repository import UserRepository
from app.models.user import UserModel
from app.models.error import Error

class UserHandler(object):
    def __init__(self, body={}, query_params={}):
        self.user = UserModel(body)
        self.query_params = query_params
        self.repository = UserRepository()

    def get(self):
        user_id = self.query_params.get('user_id')
        page = int(self.query_params.get('page', 1))
        limit = int(self.query_params.get('limit', 20))
        
        return self.repository.get(user_id=user_id, page=page, limit=limit)

    def create(self):
        if not self.user.validate():
            return Error('Invalid user data').get_400_error()

        return self.repository.create(self.user)

    def update(self):
        user_id = self.query_params.get('user_id')

        if not user_id:
            return Error("Missing 'user_id' parameter").get_400_error()

        if not self.user.validate():
            return Error('Invalid user data').get_400_error()

        return self.repository.update(user_id, self.user)

    def delete(self):
        user_id = self.query_params.get('user_id')

        if not user_id:
            return Error("Missing 'user_id' parameter").get_400_error()
        
        return self.repository.delete(user_id)