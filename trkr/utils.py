import sys

import click

def confirm(**kwargs) -> bool:
    return click.confirm([f"{k} {v} is new. Create it?" for k, v in kwargs.items()][0])


def terminate():
    click.echo("exiting without logging work")
    sys.exit(0)