import datetime

CREATE_PROJECT_SQL = """
    INSERT INTO projects (name) VALUES (?)
"""

CREATE_CLIENT_SQL = """
    INSERT INTO clients (name) VALUES (?)
"""

CREATE_WORK_LOG_SQL = """
    INSERT INTO work_log (hours, description, project_id, created_at) VALUES (?, ?, ?, ?)
"""


def create_project(cursor, *args) -> None:
    """
    Creates a new project using the provided *args

    :param cursor: database cursor
    :param args: List of args to pass to insert statement
    """
    cursor.execute(CREATE_PROJECT_SQL, args)


def update_project(cursor, project_id, **kwargs) -> None:
    """
    Updates an existing project using the provided *args

    :param cursor: database cursor
    :param project_id: project id
    :param kwargs: Key, value pairs to use while updating the record
    """
    update_stmt = ', '.join(f'{k} = ?' for k in kwargs.keys())

    update_project_sql = f"""
        UPDATE projects SET {update_stmt} WHERE id = ?
    """
    cursor.execute(update_project_sql, tuple(kwargs.values()) + (project_id, ))


def create_client(cursor, *args) -> None:
    """
    Creates a new client

    :param cursor: database cursor
    :param args: List of args to pass to insert statement
    """
    cursor.execute(CREATE_CLIENT_SQL, args)


def create_work_log(cursor, hours: float, description: str, project_id: int, created_at: str=None) -> None:
    """
    Creates a new work log row.

    :param cursor: SQLite connection cursor
    :param hours: Number of hours for work log item
    :param description: Description of what was done
    :param project_id: ID of project to connect work log item to
    :param created_at: optional timestamp to use to specify when log was created
    """
    if not created_at:
        created_at = datetime.datetime.now()
    else:
        created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d')

    cursor.execute(CREATE_WORK_LOG_SQL, (hours, description, project_id, created_at))
