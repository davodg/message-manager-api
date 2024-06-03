from config import Config
import psycopg2cffi

class Postgres(object):
    def __init__(self):
        self.config = Config()
        self.conn = psycopg2cffi.connect(
            user=self.config.postgres_db_user,
            password=self.config.postgres_db_password,
            host=self.config.postgres_db_host,
            port=self.config.postgres_db_port,
            database=self.config.postgres_db_name
        )
        self.cursor = self.conn.cursor()

    def query(self, query, values=''):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def execute(self, query, values=''):
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.fetchall() if 'RETURNING' in query else None

    def close(self):
        self.cursor.close()
        self.conn.close()