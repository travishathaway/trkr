
GET_PROJECT_BY_NAME_SQL = """
    SELECT id, name FROM projects WHERE name = ?
"""


def get_project_by_name(cursor, *args) -> tuple:
    """
    Gets a project from the database using the name.

    :param cursor: database cursor
    :param args: List of args to pass to insert statement
    """
    res = cursor.execute(GET_PROJECT_BY_NAME_SQL, args)

    return res.fetchone()
