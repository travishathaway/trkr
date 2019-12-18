
CREATE_PROJECT_SQL = """
    INSERT INTO projects (name) VALUES (?)
"""

CREATE_WORK_LOG_SQL = """
    INSERT INTO work_log (hours, description, project_id) VALUES (?, ?, ?)
"""


def create_project(cursor, *args) -> None:
    """
    Creates a new project using the provided *args

    :param cursor: database cursor
    :param args: List of args to pass to insert statement
    """
    cursor.execute(CREATE_PROJECT_SQL, args)


def create_work_log(cursor, hours: float, description: str, project_id: int) -> None:
    """
    Creates a new work log row.

    :param cursor: SQLite connection cursor
    :param hours: Number of hours for work log item
    :param description: Description of what was done
    :param project_id: ID of project to connect work log item to
    """
    cursor.execute(CREATE_WORK_LOG_SQL, (hours, description, project_id))
