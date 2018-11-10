"""
Tests of Package-Builder utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_utils.py
# pylint --disable=locally-disabled test_utils.py

import pytest
from pkgbld.utils import call, call_output


def test_call():
    """
    Test utils call function.
    """
    call('hostname')
    with pytest.raises(OSError):
        call('illegal_os_command')


def test_call_output():
    """
    Test utils call_output function.
    """
    out = call_output('hostname')
    assert len(out) > 0
    with pytest.raises(OSError):
        call_output('illegal_os_command')
