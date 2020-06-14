from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, ProgrammingError


def db_connect(db_name):

    connection = connect(
        user='postgres',
        password='coderslab',
        host='localhost',
        database = db_name
    )
    connection.autocommit = True
    return connection
