import os
import sqlite3

from trkr.constants import DB_FILE_NAME

from .schema import create_schema


def get_database_file() -> str:
    """
    Retrieves the filename used to store data
    """
    home_dir = os.path.expanduser('~')

    return os.path.join(home_dir, f'.{DB_FILE_NAME}')


def get_connection():
    """
    Returns a cursor connected to our database. If the database
    file doesn't exist, create the schema for our database too

    :return: sqlite3.connection
    """
    create_tables = False
    db_file = get_database_file()

    if not os.path.exists(db_file):
        create_tables = True

    conn = sqlite3.connect(db_file)

    if create_tables:
        create_schema(conn.cursor())
        conn.commit()

    return conn
