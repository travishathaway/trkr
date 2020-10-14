import click

from trkr.constants import DEFAULT_PROJECT_NAME
from trkr.utils import confirm, terminate
from trkr.data.connect import get_connection
from trkr.data.write import (
    create_project,
    create_work_log,
    create_client,
    update_project,
)
from trkr.data.read import get_project_by_name, get_client


@click.command()
@click.option("--hours", "-h", default=0, help="Add hours to a Project", type=click.INT)
@click.option(
    "--description",
    "-d",
    default="",
    help="Provide a description for your project",
    type=click.STRING,
)
@click.option(
    "--project",
    "-p",
    default=DEFAULT_PROJECT_NAME,
    help="Project name (default used if none provided)",
    type=click.STRING,
    required=True,
)
@click.option(
    "--client",
    "-c",
    default=None,
    help="Client to associate project with (default is none)",
    type=click.STRING,
)
# I would prefer this take in a datetime and handle the formatting using click.DATETIME which handles more edge cases
@click.option(
    "--created-at",
    "-d",
    default=None,
    help="Override the created_at field (defaults to now)",
    type=click.STRING,
)
def add(hours, description, project, client, created_at):
    """
    Adds a new work log item
    """
    conn = get_connection()
    cur = conn.cursor()

    proj = get_or_create(conn, cur, project)
    if client_rec := get_client(cur, client) is None and client:
        if confirm(client=client):
            create_client(cur, client)
            conn.commit()
            update_project(cur, project_id=proj[0], client_id=client_rec[0])
        else:
            terminate()

    create_work_log(cur, hours, description, proj[0], created_at=created_at)
    conn.commit()


def get_or_create(conn, cur, project) -> tuple:
    if proj := get_project_by_name(cur, project):
        return proj
    else:
        if confirm(project=project):
            create_project(cur, project)
            conn.commit()
            proj = get_project_by_name(cur, project)
            return proj
        else:
            terminate()
