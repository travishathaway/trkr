import sys
import os

import click
from xhtml2pdf import pisa
from jinja2 import Template

from trkr.data.connect import get_connection
from trkr.data.read import get_all_projects, get_all_logs

TEMPLATE_DIR = os.path.dirname(__file__) + '/../templates/'
REPORT_TEMPLATE = os.path.join(TEMPLATE_DIR, 'report.html')


# @click.option('-d', '--data-type', default=TYPE_PROJECT,
#               help='Type of data to show ("project" or "log"). Defaults to "project"')
# @click.option('-p', '--project', default=None,
#               help='Project name to filter by (optional)')
@click.command()
@click.argument('output', nargs=1)
@click.option('-p', '--project', default=None,
              help='Project name to filter by (optional)')
def report(output, project):
    """Generate reports from work logs"""
    if not os.path.basename(output).lower().endswith('pdf'):
        click.echo("Please give output file *.pdf extension")
        sys.exit(1)

    conn = get_connection()
    cur = conn.cursor()

    with open(REPORT_TEMPLATE) as template:
        source_html = template.read()

    project_logs = get_all_logs(cur, project=project)
    template = Template(source_html)
    html = template.render(logs=project_logs)

    with open(output, "w+b") as result_file:
        status = pisa.CreatePDF(
            html,
            dest=result_file
        )

    if status.err:
        click.echo("Errors while creating pdf")
        sys.exit(1)