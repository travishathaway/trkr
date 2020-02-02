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

GET_ALL_CLIENTS_SQL = """
    SELECT id, name FROM clients
"""

GET_CLIENT_SQL = """
    SELECT id, name FROM clients WHERE name = ?
"""

INVOICE_ITEMS_SQL = f"""
    SELECT 
        p.display_name, sum(wl.hours)
    FROM 
        work_log wl
    LEFT JOIN
        projects p
    ON
        p.id = wl.project_id
    LEFT JOIN
        clients c
    ON
        c.id = p.client_id
    WHERE
        c.name = ?
    AND
        wl.created_at BETWEEN ? AND ?
    GROUP BY
        p.display_name
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


def get_all_clients(cursor) -> tuple:
    """
    Returns all clients

    :param cursor: database cursor (SQLite)
    :param project: optionally filter logs by  project
    """
    res = cursor.execute(GET_ALL_CLIENTS_SQL)

    return res.fetchall()


def get_client(cursor, client_name) -> tuple:
    """
    Returns all clients

    :param cursor: database cursor (SQLite)
    :param client_name: client name
    """
    res = cursor.execute(GET_CLIENT_SQL, (client_name,))

    return res.fetchone()


def get_invoice_items(cursor, client_name, from_date, to_date) -> tuple:
    """
    Collect invoice items to present in a report. This invoice items are
    simply the aggregated hours by project for the time period specified.

    :param cursor:
    :param client_name: Client name to collect invoice for
    :param from_date: Begin date of the invoice
    :param to_date: End date of the invoice
    :return: tuple
    """
    res = cursor.execute(INVOICE_ITEMS_SQL, (client_name, from_date, to_date))

    return res.fetchall()
