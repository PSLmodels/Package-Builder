#!/usr/bin/env python

import logging
import os
import sys
import traceback

import click

from .config import get_packages, setup_logging
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
@u.required_commands("anaconda", "conda", "git", "tar", "tsort")
def cli(ctx):
    """
    Manage Open Source Policy Center (OSPC) packages.
    """
    ctx.obj = {}


@cli.command(short_help="Build packages.")
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--channel", "-c",
              default="ospc",
              show_default=True,
              required=False)
@click.option('--only-last', is_flag=True)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def build(ctx, names, channel, only_last, workdir, verbose):
    setup_logging(verbose)

    for pkg in get_packages(names, workdir, only_last):
        pkg.pull()
        pkg.build(channel)


@cli.command(short_help='Release packages.')
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--channel", "-c",
              default="ospc",
              show_default=True,
              required=False)
@click.option("--label", "-l",
              default="dev",
              show_default=True,
              required=False)
@click.option("--user", "-u",
              default=None,
              show_default=True,
              required=False)
@click.option('--force', is_flag=True)
@click.option('--only-last', is_flag=True)
@click.option('--token',
              envvar='OSPC_ANACONDA_TOKEN',
              default=default_token_config)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def release(ctx, names, channel, label, user, force, only_last, token, workdir, verbose):
    setup_logging(verbose)

    if token or is_authenticated_user():
        pkgs = get_packages(names, workdir, only_last)
        for pkg in pkgs:
            pkg.pull()
            pkg.build(channel)
        for pkg in pkgs:
            pkg.upload(token, label, user, force)


@cli.command(short_help='Upload packages.')
@click.pass_context
@click.argument('names', nargs=-1)
@click.option("--label", "-l",
              default="dev",
              show_default=True,
              required=False)
@click.option("--user", "-u",
              default=None,
              show_default=True,
              required=False)
@click.option('--force', is_flag=True)
@click.option('--only-last', is_flag=True)
@click.option('--token',
              envvar='OSPC_ANACONDA_TOKEN',
              default=default_token_config)
@click.option("--workdir", "-w",
              default="/tmp",
              show_default=True,
              required=False)
@click.option('-v', '--verbose', count=True)
def upload(ctx, names, label, user, force, only_last, token, workdir, verbose):
    setup_logging(verbose)

    if token or is_authenticated_user():
        for pkg in get_packages(names, workdir, only_last):
            pkg.upload(token, label, user, force)


if __name__ == '__main__':
    start()
