import sys

import click

from trkr.constants import DEFAULT_PROJECT_NAME
from trkr.data.connect import get_connection
from trkr.data.write import create_project, create_work_log
from trkr.data.read import get_project_by_name


@click.command()
@click.argument('hours', nargs=1)
@click.argument('description', nargs=1)
@click.option('--project', default=DEFAULT_PROJECT_NAME,
              help='Project name (default used if none provided)')
def add(hours, description, project):
    """
    Adds a new work log item
    """
    conn = get_connection()
    cur = conn.cursor()

    # This get or create proj block could be its own function
    proj = get_project_by_name(cur, project)

    if not proj:
        if click.confirm(f'Project {project} does not exist. create it?'):
            create_project(cur, project)
            conn.commit()
            proj = get_project_by_name(cur, project)
        else:
            click.echo("exiting without logging work")
            sys.exit(0)

    create_work_log(cur, hours, description, proj[0])
    conn.commit()
