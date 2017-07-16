import logging
import logging.handlers
import sys


def setup_logging(log_level=logging.WARNING):
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


def get_packages(names):
    if not names:
        return ('taxcalc', 'btax', 'ogusa')
    return names
