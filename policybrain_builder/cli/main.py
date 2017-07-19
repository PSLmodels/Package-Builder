#!/usr/bin/env python

import logging
import os
import sys
import traceback

import click

from .config import setup_logging
from .package import get_packages
from . import utils as u


logger = logging.getLogger(__name__)


def start():
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("Interrupted by Ctrl-C.")
        sys.exit(1)
    except Exception:
        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


def is_authenticated_user():
    output = u.check_output("anaconda whoami")
    if "anonymous" not in output.lower():
        click.secho("ERROR: cannot upload packages when Anaconda user is anonymous", fg="red")
        click.secho("To resolve, log in as an authenticated user or provide a token", fg="red")
        return False
    return True


def default_token_config():
    path = os.path.join(os.path.expanduser('~'), '.ospc_anaconda_token')
    if os.path.exists(path):
        return path
    return None


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name="pb", version="0.0.1")
@click.pass_context
@u.required_commands("anaconda", "conda", "git", "tsort")
def cli(ctx):
    """
    Manage Open Source Policy Center (OSPC) packages.
    """
    ctx.obj = {}


@cli.command(short_help="Build packages.")
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--tag",
              default=None,
              show_default=True,
              required=False)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def build(ctx, names, tag, workdir, verbose):
    setup_logging(verbose)

    for pkg in get_packages(names, workdir):
        pkg.pull(tag)
        pkg.build()


@cli.command(short_help='Display information about packages.')
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def info(ctx, names, workdir, verbose):
    setup_logging(verbose)

    for pkg in get_packages(names, workdir):
        click.echo("looking for {}".format(click.style(pkg.name, fg='green')))


@cli.command(short_help='Release packages.')
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--tag",
              default=None,
              show_default=True,
              required=False)
@click.option('--token',
              envvar='OSPC_ANACONDA_TOKEN',
              default=default_token_config)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def release(ctx, names, tag, token, workdir, verbose):
    setup_logging(verbose)

    if token or is_authenticated_user():
        pkgs = get_packages(names, workdir)
        for pkg in pkgs:
            pkg.pull(tag)
            pkg.build()
        for pkg in pkgs:
            pkg.upload()


@cli.command(short_help='Upload packages.')
@click.pass_context
@click.argument('names', nargs=-1)
@click.option('--token',
              envvar='OSPC_ANACONDA_TOKEN',
              default=default_token_config)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def upload(ctx, names, token, workdir, verbose):
    setup_logging(verbose)

    if token or is_authenticated_user():
        for pkg in get_packages(names, workdir):
            pkg.upload()


if __name__ == '__main__':
    start()
