"""
Tests of Package-Builder utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_utils.py
# pylint --disable=locally-disabled test_utils.py

import pytest
from pkgbld.utils import os_call, os_call_output


def test_os_call():
    """
    Test call utility function.
    """
    os_call('hostname')
    with pytest.raises(OSError):
        os_call('illegal_os_command')


def test_os_call_output():
    """
    Test call_output utility function.
    """
    out = os_call_output('hostname')
    assert out
    with pytest.raises(OSError):
        out = os_call_output('illegal_os_command')
