# -*- coding: utf-8 -*-

"""Top-level package for CLI App"""

import click

from trkr import commands


__author__ = """Travis Hathaway"""
__email__ = "travis@example.com"
__version__ = "0.1.0"


@click.group()
def cli():
    pass


# Add commands
cli.add_command(commands.show)
cli.add_command(commands.add)
cli.add_command(commands.report)
