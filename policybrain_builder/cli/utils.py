import contextlib
import functools
import logging
import os
import re
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
def set_and_rollback_conda_config(key, value):
    args = check_output("conda config --get " + key)
    logger.info("saved previous conda config: %s", key)
    try:
        call("conda config --set {} {}".format(key, value))
        logger.info("changed conda config: %s %s", key, value)
        yield
    finally:
        call("conda config " + args)
        logger.info("restored previous conda config: %s", key)


@contextlib.contextmanager
def change_working_directory(path):
    old_path = os.getcwd()
    logger.info("saved previous working directory: %s", old_path)
    try:
        os.chdir(path)
        logger.info("changed working directory: %s", path)
        yield
    finally:
        os.chdir(old_path)
        logger.info("restored previous working directory: %s", old_path)


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
        logger.info("creating directory: %s", path)
        os.makedirs(path)


def find_first_filename(path, *filenames):
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return filename
    return None


def replace_all(filename, needle, replacement):
    logger.info("replacing all relevant lines in %s", filename)
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(re.sub(needle, replacement, line))
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line)
