import sys

import click

from trkr.constants import DEFAULT_PROJECT_NAME
from trkr.data.connect import get_connection
from trkr.data.write import (
    create_project, create_work_log, create_client, update_project
)
from trkr.data.read import get_project_by_name, get_client


@click.command()
@click.argument('hours', nargs=1)
@click.argument('description', nargs=1)
@click.option('--project', '-p', default=DEFAULT_PROJECT_NAME,
              help='Project name (default used if none provided)')
@click.option('--client', '-c', default=None,
              help='Client to associate project with (default is none)')
@click.option('--created-at', '-d', default=None,
              help='Override the created_at field (defaults to now)')
def add(hours, description, project, client, created_at):
    """
    Adds a new work log item
    """
    conn = get_connection()
    cur = conn.cursor()

    # This get or create proj block could be its own function
    proj = get_project_by_name(cur, project)
    client_rec = get_client(cur, client) if client else None

    if not proj:
        if click.confirm(f'Project {project} does not exist. create it?'):
            create_project(cur, project)
            conn.commit()
            proj = get_project_by_name(cur, project)
        else:
            click.echo("exiting without logging work")
            sys.exit(0)

    if not client_rec and client is not None:
        if click.confirm(f'Client {client} does not exist. create it?'):
            create_client(cur, client)
            conn.commit()
            client_rec = get_client(cur, client)
            update_project(cur, project_id=proj[0], client_id=client_rec[0])
        else:
            click.echo("exiting without logging work")
            sys.exit(0)

    create_work_log(cur, hours, description, proj[0], created_at=created_at)
    conn.commit()
