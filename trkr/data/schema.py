from trkr.constants import DEFAULT_PROJECT_NAME

WORK_LOG_TABLE_DDL = """
CREATE TABLE work_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    hours FLOAT,
    project_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

PROJECT_TABLE_DDL = """
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    client_id INTEGER
)
"""

CLIENT_TABLE_DDL = """
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
"""


def create_schema(cursor) -> None:
    """
    Creates all the tables necessary for our schema

    :param cursor: sqllite3 cursor
    """
    cursor.execute(PROJECT_TABLE_DDL)
    cursor.execute(CLIENT_TABLE_DDL)
    cursor.execute(WORK_LOG_TABLE_DDL)

    # Insert the default project
    cursor.execute('INSERT INTO projects (name) VALUES (?)', (DEFAULT_PROJECT_NAME, ))


def delete_schema(cursor) -> None:
    """
    Deletes all the tables... all of em!

    :param cursor: sqllite3 cursor
    """
    cursor.execute("DROP TABLE projects")
    cursor.execute("DROP TABLE clients")
    cursor.execute("DROP TABLE work_log")
