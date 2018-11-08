#!/usr/bin/env python

import logging
import os
import sys
import traceback

import click

from . import config
from . import utils as u


logger = logging.getLogger(__name__)


def start():
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("Interrupted by Ctrl-C")
        sys.exit(1)
    except Exception:
        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


def is_authenticated_user():
    output = u.check_output("anaconda whoami")
    if "anonymous" not in output.lower():
        click.secho(("ERROR: cannot upload packages when Anaconda user "
                    "is anonymous"), fg="red")
        click.secho(("To resolve, log in as an authenticated user "
                     "or provide a token"), fg="red")
        return False
    return True


def default_token_config():
    path = os.path.expanduser("~/.pslmodels_anaconda_token")
    if os.path.exists(path):
        return path
    return None


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name="pb", version="0.7.0")
@click.pass_context
@u.required_commands("anaconda", "conda", "git", "tar", "tsort")
def cli(ctx):
    """
    Manage Policy Simulation Library (PSL) packages.
    """
    ctx.obj = {}


@cli.command(short_help="Build packages.")
@click.pass_context
@click.argument("names", nargs=-1)
@click.option("--channel", "-c",
              envvar="PSLMODELS_ANACONDA_CHANNEL",
              default="pslmodels",
              show_default=True,
              required=False)
@click.option("--only-last", is_flag=True)
@click.option("--python",
              envvar="PSLMODELS_PYTHON_VERSIONS",
              default=lambda: config.PYTHON_VERSIONS,
              show_default=False,
              multiple=True,
              required=False,
              help="[default: " + " ".join(config.PYTHON_VERSIONS) + "]")
@click.option("--workdir", "-w",
              envvar="WORKDIR",
              default=os.path.expanduser("~/tmp/Package-Builder"),
              show_default=True,
              required=False)
@click.option("--clean",
              is_flag=True,
              help="Remove working directory upon start.")
@click.option("-v", "--verbose", count=True)
def build(ctx, names, channel, only_last, python, workdir, clean, verbose):
    config.setup_logging(verbose)
    with u.set_and_rollback_conda_config("always_yes", True):
        cache_dir = config.get_package_cache_directory(workdir)
        u.ensure_directory_exists(cache_dir, clean)
        for pkg in config.get_packages(names, workdir, only_last):
            pkg.pull()
            pkg.build(channel, py_versions)


@cli.command(short_help="Release packages.")
@click.pass_context
@click.argument("names", nargs=-1)
@click.option("--channel", "-c",
              envvar="PSLMODELS_ANACONDA_CHANNEL",
              default="pslmodels",
              show_default=True,
              required=False)
@click.option("--label", "-l",
              envvar="PSLMODELS_ANACONDA_LABEL",
              default="main",
              show_default=True,
              required=False)
@click.option("--user", "-u",
              default=None,
              show_default=True,
              required=False)
@click.option("--force",
              envvar="ANACONDA_FORCE",
              is_flag=True)
@click.option("--only-last", is_flag=True)
@click.option("--python",
              envvar="PSLMODELS_PYTHON_VERSIONS",
              default=lambda: config.PYTHON_VERSIONS,
              show_default=False,
              multiple=True,
              required=False,
              help="[default: " + " ".join(config.PYTHON_VERSIONS) + "]")
@click.option("--token",
              envvar="PSLMODELS_ANACONDA_TOKEN",
              default=default_token_config)
@click.option("--workdir", "-w",
              envvar="WORKDIR",
              default=os.path.expanduser("~/tmp/Package-Builder"),
              show_default=True,
              required=False)
@click.option("--clean",
              is_flag=True,
              help="Remove working directory upon start.")
@click.option("-v", "--verbose", count=True)
def release(ctx, names, channel, label, user, force, only_last,
            python, token, workdir, clean, verbose):
    config.setup_logging(verbose)
    if token or is_authenticated_user():
        with u.set_and_rollback_conda_config("always_yes", True):
            cache_dir = config.get_package_cache_directory(workdir)
            u.ensure_directory_exists(cache_dir, clean)
            pkgs = config.get_packages(names, workdir, only_last)
            for pkg in pkgs:
                pkg.pull()
                pkg.build(channel, python)
            for pkg in pkgs:
                pkg.upload(token, label, python, user, force)


@cli.command(short_help="Upload packages.")
@click.pass_context
@click.argument("names", nargs=-1)
@click.option("--label", "-l",
              envvar="PSLMODELS_ANACONDA_LABEL",
              default="main",
              show_default=True,
              required=False)
@click.option("--user", "-u",
              default=None,
              show_default=True,
              required=False)
@click.option("--force",
              envvar="ANACONDA_FORCE",
              is_flag=True)
@click.option("--only-last", is_flag=True)
@click.option("--python",
              envvar="PSLMODELS_PYTHON_VERSIONS",
              default=lambda: config.PYTHON_VERSIONS,
              show_default=False,
              multiple=True,
              required=False,
              help="[default: " + " ".join(config.PYTHON_VERSIONS) + "]")
@click.option("--token",
              envvar="PSLMODELS_ANACONDA_TOKEN",
              default=default_token_config)
@click.option("--workdir", "-w",
              envvar="WORKDIR",
              default=os.path.expanduser("~/tmp/Package-Builder"),
              show_default=True,
              required=False)
@click.option("--clean",
              is_flag=True,
              help="Remove working directory upon start.")
@click.option("-v", "--verbose", count=True)
def upload(ctx, names, label, user, force, only_last, python,
           token, workdir, clean, verbose):
    config.setup_logging(verbose)
    if token or is_authenticated_user():
        with u.set_and_rollback_conda_config("always_yes", True):
            cache_dir = config.get_package_cache_directory(workdir)
            u.ensure_directory_exists(cache_dir, clean)
            for pkg in config.get_packages(names, workdir, only_last):
                pkg.upload(token, label, python, user, force)


if __name__ == "__main__":
    start()
