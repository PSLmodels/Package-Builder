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
    pkgs = {
        'taxcalc': Package(
            'taxcalc',
            Repository(
                'https://github.com/open-source-economics/Tax-Calculator',
                os.path.join(workdir, 'src', 'taxcalc')),
            os.path.join(workdir, 'pkg')),
        'btax': Package(
            'btax',
            Repository(
                'https://github.com/open-source-economics/B-Tax',
                os.path.join(workdir, 'src', 'btax')),
            os.path.join(workdir, 'pkg')),
        'ogusa': Package(
            'ogusa',
            Repository(
                'https://github.com/open-source-economics/OG-USA',
                os.path.join(workdir, 'src', 'ogusa')),
            os.path.join(workdir, 'pkg'))}
    keys = names if names else pkgs.keys()
    return [pkgs[name] for name in keys]
