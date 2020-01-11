import sys

import click
from tabulate import tabulate

from trkr.data.connect import get_connection
from trkr.data.read import get_all_projects, get_all_logs

LIST_FIELDS_PROJECTS = ('id', 'name', 'total_hours')
LIST_FIELDS_LOGS = ('name', 'description', 'hours', 'when')

TYPE_PROJECT = 'project'
TYPE_LOG = 'log'


@click.command()
@click.option('-d', '--data-type', default=TYPE_PROJECT,
              help='Type of data to show ("project" or "log"). Defaults to "project"')
@click.option('-p', '--project', default=None,
              help='Project name to filter by (optional)')
def show(data_type, project):
    """
    Shows the available projects
    """
    conn = get_connection()
    cur = conn.cursor()

    if data_type == TYPE_PROJECT:
        data = get_all_projects(cur)
        headers = LIST_FIELDS_PROJECTS
    elif data_type == TYPE_LOG:
        data = get_all_logs(cur, project)
        headers = LIST_FIELDS_LOGS
    else:
        click.echo(f"Invalid type, available choices are '{TYPE_PROJECT}' and '{TYPE_LOG}'")
        sys.exit(1)

    click.echo(tabulate(data, headers=headers))
