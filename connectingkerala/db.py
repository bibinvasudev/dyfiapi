from mongoengine import connect
from mongoengine.connection import disconnect

__all__ = ('setup_connection',)

DB_CONNECTION_STRING = "mongodb://localhost/conn_kerala"
DB_REPLICA_SET = {}


def setup_connection():

    # Disconnect any previous session if any
    disconnect(alias=DB_CONNECTION_STRING)

    try:
        connect(host=DB_CONNECTION_STRING, **DB_REPLICA_SET)
    except ConnectionError as conn_exc:
        print('DB Error: {}'.format(str(conn_exc)))
        exit(1)
