import psycopg2
import psycopg2.extras


class Connection:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        conn = psycopg2.connect("database, user, password, host, port")
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute()


