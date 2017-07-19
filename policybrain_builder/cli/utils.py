import contextlib
import functools
import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)


def required_commands(*commands):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            """
            Fails if any required command is not available
            """
            failed = False
            for command in commands:
                try:
                    # Unix-specific command lookup
                    check_output("which {}".format(command))
                except subprocess.CalledProcessError:
                    logger.error("Required command does not exist: %s", command)
                    failed = True
            if failed:
                sys.exit(1)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@contextlib.contextmanager
def change_working_directory(path):
    old_path = os.getcwd()
    logger.debug("saved previous working directory: %s", old_path)
    try:
        os.chdir(path)
        logger.debug("changed working directory: %s", path)
        yield
    finally:
        os.chdir(old_path)
        logger.debug("restored previous working directory: %s", old_path)


def call(cmd):
    logger.debug(cmd)
    subprocess.check_call(cmd, shell=True)


def check_output(cmd):
    logger.debug(cmd)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        output = str(e)
    return output


def ensure_directory_exists(path):
    if not os.path.exists(path):
        logger.debug("creating directory: %s", path)
        os.makedirs(path)
