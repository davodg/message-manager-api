from app.services.postgres import Postgres
from app.models.user import UserModel
from datetime import datetime

class UserRepository(object):
    def __init__(self):
        self.postgres = Postgres()
        self.context = {'status': '200 OK', 'data': {}, 'meta': {}}

    def get(self, page, limit, user_id=''):
        offset = (page - 1) * limit
        users = []

        query = "SELECT count(*) FROM users"
        total_users = self.postgres.query(query)

        self.context['meta']['total'] = total_users[0][0]
        self.context['meta']['page'] = page
        self.context['meta']['limit'] = limit

        query = """
        SELECT json_agg(t) FROM ( 
        SELECT id, name, email, phone, age, TO_CHAR(creation_date, 'YYYY-MM-DD HH24:MI:SS') as creation_date, 
        TO_CHAR(update_date, 'YYYY-MM-DD HH24:MI:SS') as update_date FROM users
        ) t
        """

        if user_id:
            query += " WHERE id = '{}'".format(user_id)
        
        query += " LIMIT {} OFFSET {}".format(limit, offset)
        
        users_data = self.postgres.query(query)

        if users_data:
            users_data = users_data[0][0]
            for user_data in users_data:
                user = UserModel(user_data)
                users.append(user.to_dict())

        self.context['data'] = users

        return self.context

    def create(self, user):
        query = 'INSERT INTO users (name, email, phone, age) VALUES (%s, %s, %s, %s) RETURNING id, creation_date'
        values = (user.name, user.email, user.phone, user.age)

        user_data = self.postgres.execute(query, values)
        user.id = user_data[0][0]
        user.creation_date = user_data[0][1].isoformat()

        self.context['data'] = user.to_dict()
        self.context['status'] = '201 Created'

        return self.context

    def update(self, user_id, user):
        query = "UPDATE users SET name = %s, email = %s, phone = %s, age = %s, update_date = %s WHERE id = %s RETURNING id, creation_date, update_date"
        values = (user.name, user.email, user.phone, user.age, datetime.now(), user_id)

        user_data = self.postgres.execute(query, values)
        user.id = user_data[0][0]
        user.creation_date = user_data[0][1].isoformat()
        user.update_date = user_data[0][2].isoformat()

        self.context['data'] = user.to_dict()

        return self.context

    def delete(self, user_id):
        query = "DELETE FROM users WHERE id = '%s'"

        self.postgres.execute(query % user_id)

        return self.context
        