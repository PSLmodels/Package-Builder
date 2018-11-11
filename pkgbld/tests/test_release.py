"""
Tests of Package-Builder release function.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_release.py
# pylint --disable=locally-disabled test_release.py

import pytest
from pkgbld.release import release


@pytest.mark.parametrize('rname, pname, version',
                         [(28, 'taxcalc', '0.23.0'),
                          ("Tax-Calculator", 28, '0.23.0'),
                          ("Tax-Calculator", 'taxcalc', 28),
                          ("Tax-Calculator", 'taxcalc', '0.23'),
                          ("Tax-Calculator", 'taxcalc', '0.23.0rc1')])
def test_improper_release_calls(rname, pname, version):
    """
    Test release calls that generate a ValueError.
    """
    with pytest.raises(ValueError):
        release(rname, pname, version)
