import subprocess
import sys
import platform
"""
import contextlib
import os
import shutil
"""


def call(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        raise(OSError)
        sys.exit(e.returncode)


def call_output(cmd):
    try:
        output = subprocess.check_output(cmd,
                                         stderr=subprocess.STDOUT,
                                         shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        raise(OSError)
        sys.exit(e.returncode)
    return output


def conda_os_name():
    system_ = platform.system()
    if system_ == 'Darwin':
        conda_name = 'osx'
    elif system_ == 'Linux':
        conda_name = 'linux'
    elif system_ == 'Windows':
        conda_name = 'win'
    else:
        msg = 'OS=<{}> is not Windows, Linux, or Darwin(OSX).'
        raise OSError(msg.format(system_))
    # For following bit-size code, see this link:
    # https://docs.python.org/3.6/library/platform.html#platform.architecture
    is_64bit = sys.maxsize > 2 ** 32
    n_bits = '64' if is_64bit else '32'
    return conda_name + '-' + n_bits


"""
def required_commands(*commands):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Fails if any required command is not available
            failed = False
            for command in commands:
                try:
                    # Unix-specific command lookup
                    check_output("which {}".format(command))
                except subprocess.CalledProcessError:
                    msg = "Required command does not exist: %s"
                    logger.error(msg, command)
                    failed = True
            if failed:
                sys.exit(1)
            return f(*args, **kwargs)
        return wrapper
    return decorator
"""


"""
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


def get_current_os():
    # Get the system corresponding to OPERATING_SYSTEMS
    system_ = platform.system()
    if system_ == 'Darwin':
        conda_name = 'osx'
    elif system_ == 'Linux':
        conda_name = 'linux'
    elif system_ == 'Windows':
        conda_name = 'win'
    else:
        msg = ("The user is using an unexpected operating system: {}.\n"
               "Expected operating systems are windows, linux, or osx.")
        raise OSError(msg.format(system_))
    # see link:
    # https://docs.python.org/3.6/library/platform.html#platform.architecture
    is_64bit = sys.maxsize > 2 ** 32
    n_bits = '64' if is_64bit else '32'
    return conda_name + '-' + n_bits


def ensure_directory_exists(path, clean=False):
    if clean and os.path.exists(path):
        logger.info("removing directory: %s", path)
        shutil.rmtree(path)
    if not os.path.exists(path):
        logger.info("creating directory: %s", path)
        os.makedirs(path)


def replace_all(filename, needle, replacement):
    lines = list()
    with open(filename) as f:
        for line in f.readlines():
            lines.append(re.sub(needle, replacement, line))
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)


def find_first_filename(path, *filenames):
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return filename
    return None
"""
