import sys
import os
from datetime import datetime

import click
from xhtml2pdf import pisa
from jinja2 import Template

from trkr.data.connect import get_connection
from trkr.data.read import get_all_projects, get_all_logs

TEMPLATE_DIR = os.path.dirname(__file__) + '/../templates/'
REPORT_TEMPLATE = os.path.join(TEMPLATE_DIR, 'report.html')


@click.command()
@click.argument('output', nargs=1)
@click.option('-p', '--project', default=None,
              help='Project name to filter by (optional)')
@click.option('-c', '--company-name', default=None,
              help='Company name to display on invoice')
@click.option('-i', '--invoice-id', default=None,
              help='ID to associate with the invoice')
@click.option('-t', '--client-name', default=None,
              help='Company to bill invoice to')
@click.option('--addr-line-1', default=None,
              help='Company name address line 1')
@click.option('--addr-line-2', default=None,
              help='Company name address line 2')
def report(**kwargs):
    """Generate reports from work logs"""
    output = kwargs.get('output', '')
    project = kwargs.get('project')

    if not os.path.basename(output).lower().endswith('pdf'):
        click.echo("Please give output file *.pdf extension")
        sys.exit(1)

    conn = get_connection()
    cur = conn.cursor()

    with open(REPORT_TEMPLATE) as template:
        source_html = template.read()

    project_logs = get_all_logs(cur, project=project)
    template = Template(source_html)
    today = datetime.today()
    today_str = today.strftime('%x')
    html = template.render(logs=project_logs, today_str=today_str, **kwargs)

    with open(output, "w+b") as result_file:
        status = pisa.CreatePDF(
            html,
            dest=result_file
        )

    if status.err:
        click.echo("Errors while creating pdf")
        sys.exit(1)
