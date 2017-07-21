import logging
import logging.handlers
import os
import sys

from .package import Package
from .repository import Repository
from . import utils as u


def setup_logging(verbose=0):
    if verbose > 1:
        log_level = logging.DEBUG
    elif verbose > 0:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    # Hide messages if we log before setting up handler
    logging.root.manager.emittedNoHandlerWarning = True

    logger = logging.getLogger("policybrain_builder")
    logger.setLevel(log_level)
    logger.propagate = False

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    add_handler = True
    for handle in logger.handlers:
        if getattr(handle, "stream", None) == sys.stdout:
            add_handler = False
            break
    if add_handler:
        logger.addHandler(console_handler)


def get_packages(names, workdir, only_last=None):
    pkg_cache_dir = os.path.join(workdir, 'policybrain-builder')

    pkgs = {}

    pkgs['taxcalc'] = Package(
        name='taxcalc',
        repo=Repository('https://github.com/open-source-economics/Tax-Calculator'),
        cachedir=pkg_cache_dir)

    pkgs['btax'] = Package(
        name='btax',
        repo=Repository('https://github.com/open-source-economics/B-Tax'),
        dependencies=[pkgs['taxcalc']],
        cachedir=pkg_cache_dir)

    pkgs['ogusa'] = Package(
        name='ogusa',
        repo=Repository('https://github.com/open-source-economics/OG-USA'),
        dependencies=[pkgs['taxcalc']],
        cachedir=pkg_cache_dir)

    if not names:
        names = pkgs.keys()

    dag = ""
    for name in names:
        fields = name.split('=')
        if len(fields) == 1:
            fields.append(None)
        key, tag = fields
        pkgs[key].tag = tag
        if pkgs[key].dependencies:
            for pkg in pkgs[key].dependencies:
                dag += "{} {} ".format(key, pkg.name)
        else:
            dag += "{} . ".format(key)

    # Topological sort of package dependencies
    output = u.check_output("echo '{}' | tsort | xargs".format(dag))
    keys = list(reversed(output.strip().split()))

    # Remove sentinel marker (aka '.') if it exists
    if keys[0] == '.':
        keys = keys[1:]

    if only_last:
        keys = keys[-1:]

    return [pkgs[name] for name in keys]
