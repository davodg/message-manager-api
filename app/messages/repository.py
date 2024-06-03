from app.services.postgres import Postgres
from app.models.message import MessageModel
from datetime import datetime
import json


class MessageRepository(object):
    def __init__(self):
        self.postgres = Postgres()
        self.context = {'status': '200 OK', 'data': {}, 'meta': {}}

    def get(self, page, limit, message_id=''):
        offset = (page - 1) * limit
        messages = []

        query = "SELECT count(*) FROM messages"
        total_messages = self.postgres.query(query)

        self.context['meta']['total'] = total_messages[0][0]
        self.context['meta']['page'] = page
        self.context['meta']['limit'] = limit

        query = """
        SELECT json_agg(t) FROM (
            SELECT id, status, text, TO_CHAR(creation_date, 'YYYY-MM-DD HH24:MI:SS') as creation_date,
            TO_CHAR(update_date, 'YYYY-MM-DD HH24:MI:SS') as update_date FROM messages
        ) t
        """

        if message_id:
            query += " WHERE id = '{}'".format(message_id)

        query += " LIMIT {} OFFSET {}".format(limit, offset)

        messages_data = self.postgres.query(query)
        print(messages_data)
        messages_data = messages_data[0][0]
        print(messages_data)
        if messages_data:
            for message_data in messages_data:
                message = MessageModel(message_data)
                messages.append(message.to_dict())
        
        self.context['data'] = messages

        return self.context

    def create(self, message):
        query = 'INSERT INTO messages (status, text) VALUES (%s, %s) RETURNING id, creation_date'
        text_json = json.dumps(message.text)
        values = (message.status, text_json)

        message_data = self.postgres.execute(query, values)
        message.id = message_data[0][0]
        message.creation_date = message_data[0][1].isoformat()

        self.context['data'] = message.to_dict()
        self.context['status'] = '201 Created'

        return self.context

    def update(self, message_id, message):
        query = 'UPDATE messages SET text = %s, update_date = %s WHERE id = %s RETURNING id, update_date'
        text_json = json.dumps(message.text)
        values = (text_json, datetime.now(), message_id)

        message_data = self.postgres.execute(query, values)
        message.id = message_data[0][0]
        message.update_date = message_data[0][1].isoformat()

        self.context['data'] = message.to_dict()

        return self.context

    def delete(self, message_id):
        query = 'DELETE FROM messages WHERE id = %s'
        values = (message_id,)

        self.postgres.execute(query, values)

        return self.context