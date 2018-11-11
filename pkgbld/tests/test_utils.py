"""
Tests of Package-Builder utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_utils.py
# pylint --disable=locally-disabled test_utils.py

import pytest
from pkgbld.utils import os_call


def test_os_call():
    """
    Test call utility function.
    """
    os_call('hostname')
    with pytest.raises(OSError):
        os_call('illegal_os_command')
