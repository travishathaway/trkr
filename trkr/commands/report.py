import sys
import os
from datetime import datetime, timedelta

import click
from xhtml2pdf import pisa
from jinja2 import Template

from trkr.data.connect import get_connection
from trkr.data.read import get_invoice_items

TEMPLATE_DIR = os.path.dirname(__file__) + '/../templates/'
REPORT_TEMPLATE = os.path.join(TEMPLATE_DIR, 'report.html')

TODAY = datetime.today()
TODAY_STR = TODAY.strftime('%Y-%m-%d')
THIRTY_DAYS_BACK = TODAY - timedelta(30)
THIRTY_DAYS_BACK_STR = THIRTY_DAYS_BACK.strftime('%Y-%m-%d')


@click.command()
@click.argument('output', nargs=1)
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
@click.option('--from-date', default=THIRTY_DAYS_BACK_STR, type=click.DateTime(),
              help='Beginning date for invoice (default, 30 days ago)')
@click.option('--to-date', default=TODAY_STR, type=click.DateTime(),
              help='Beginning date for invoice (default, today)')
@click.option('--hourly-rate', default=0, type=float,
              help='Hourly rate to charge across projects (defaults to 0)')
def report(**kwargs):
    """Generate reports from work logs"""
    output = kwargs.get('output', '')

    if not os.path.basename(output).lower().endswith('pdf'):
        click.echo("Please give output file *.pdf extension")
        sys.exit(1)

    conn = get_connection()
    cur = conn.cursor()

    with open(REPORT_TEMPLATE) as template:
        source_html = template.read()

    invoice_items = get_invoice_items(
        cur, kwargs.get('client_name'), kwargs.get('from_date'), kwargs.get('to_date')
    )
    today = datetime.today()
    today_str = today.strftime('%x')
    from_str = kwargs.get('from_date').strftime('%x')
    to_str = kwargs.get('to_date').strftime('%x')
    template = Template(source_html)
    html = template.render(
        invoice_items=invoice_items, today_str=today_str, from_str=from_str, to_str=to_str,
        **kwargs
    )

    with open(output, "w+b") as result_file:
        status = pisa.CreatePDF(
            html,
            dest=result_file
        )

    if status.err:
        click.echo("Errors while creating pdf")
        sys.exit(1)
