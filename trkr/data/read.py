
GET_PROJECT_BY_NAME_SQL = """
    SELECT 
        id, name
    FROM 
        projects 
    WHERE
        name = ?
"""

GET_ALL_PROJECTS_SQL = """
    SELECT 
        projects.id, 
        projects.name, 
        sum(work_log.hours)
    FROM 
        projects 
    LEFT JOIN
        work_log
    ON
        work_log.project_id = projects.id
    GROUP BY
        projects.id, projects.name
"""

GET_ALL_LOGS_SQL = """
    SELECT 
        projects.name,
        SUBSTR(work_log.description, 0, 45),
        work_log.hours,
        work_log.created_at
    FROM 
        work_log 
    LEFT JOIN
        projects
    ON
        work_log.project_id = projects.id
"""


def get_project_by_name(cursor, *args) -> tuple:
    """
    Gets a project from the database using the name.

    :param cursor: database cursor (SQLite)
    :param args: List of args to pass to insert statement
    """
    res = cursor.execute(GET_PROJECT_BY_NAME_SQL, args)

    return res.fetchone()


def get_all_projects(cursor) -> tuple:
    """
    Returns all projects

    :param cursor: database cursor (SQLite)
    """
    res = cursor.execute(GET_ALL_PROJECTS_SQL)

    return res.fetchall()


def get_all_logs(cursor, project=None) -> tuple:
    """
    Returns all work logs

    :param cursor: database cursor (SQLite)
    :param project: optionally filter logs by  project
    """
    if project:
        sql = GET_ALL_LOGS_SQL + ' WHERE projects.name = ?'
        res = cursor.execute(sql, (project,))
    else:
        res = cursor.execute(GET_ALL_LOGS_SQL)

    return res.fetchall()
