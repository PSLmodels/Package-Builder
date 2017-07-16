#!/usr/bin/env python

import logging
import sys
import traceback

import click

from .config import setup_logging, get_packages
from .utils import required_commands


logger = logging.getLogger(__name__)


def start():
    try:
        setup_logging(logging.DEBUG)
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("Interrupted by Ctrl-C.")
        sys.exit(1)
    except Exception:
        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name="pb", version="0.0.1")
@click.pass_context
@required_commands("anaconda", "conda", "git", "tsort")
def cli(ctx):
    """
    Manage Open Source Policy Center (OSPC) packages.
    """
    ctx.obj = {}


@cli.command(short_help="Build packages.")
@click.pass_context
@click.argument('names', nargs=-1)
def build(ctx, names):
    for name in get_packages(names):
        click.echo("building {}".format(click.style(name, fg='green')))


@cli.command(short_help='Display information about packages.')
@click.pass_context
@click.argument('names', nargs=-1)
def info(ctx, names):
    for name in get_packages(names):
        click.echo("looking for {}".format(click.style(name, fg='green')))


@cli.command(short_help='Release packages.')
@click.pass_context
@click.argument('names', nargs=-1)
def release(ctx, names):
    for name in get_packages(names):
        click.echo("releasing {}".format(click.style(name, fg='green')))


@cli.command(short_help='Upload packages.')
@click.pass_context
@click.argument('names', nargs=-1)
def upload(ctx, names):
    for name in get_packages(names):
        click.echo("uploading {}".format(click.style(name, fg='green')))


if __name__ == '__main__':
    start()
