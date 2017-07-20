import logging
import logging.handlers
import os
import sys

from .package import Package
from .repository import Repository


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


def get_packages(names, workdir):
    pkg_cache_dir = os.path.join(workdir, 'pkg')
    repo_cache_dir = os.path.join(workdir, 'src')

    pkgs = {}

    pkgs['taxcalc'] = Package(
        name='taxcalc',
        repo=Repository(
            url='https://github.com/open-source-economics/Tax-Calculator',
            path=os.path.join(repo_cache_dir, 'taxcalc')),
        cachedir=pkg_cache_dir)

    pkgs['btax'] = Package(
        name='btax',
        repo=Repository(
            url='https://github.com/open-source-economics/B-Tax',
            path=os.path.join(repo_cache_dir, 'btax')),
        dependencies=[pkgs['taxcalc']],
        cachedir=pkg_cache_dir)

    pkgs['ogusa'] = Package(
        name='ogusa',
        repo=Repository(
            url='https://github.com/open-source-economics/OG-USA',
            path=os.path.join(repo_cache_dir, 'ogusa')),
        dependencies=[pkgs['taxcalc']],
        cachedir=pkg_cache_dir)

    keys = names if names else pkgs.keys()
    return [pkgs[name] for name in keys]
