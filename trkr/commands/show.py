import click
from tabulate import tabulate

from trkr.data.connect import get_connection

LIST_FIELDS = ('id', 'name')

LIST_PROJECTS = f"""
SELECT {','.join(LIST_FIELDS)} FROM projects
"""


@click.command()
def show():
    """
    Shows the available projects
    """
    conn = get_connection()
    cur = conn.cursor()
    res = cur.execute(LIST_PROJECTS)

    click.echo(tabulate(res.fetchall(), headers=LIST_FIELDS))
