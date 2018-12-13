"""
Tests of Package-Builder release function.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_release.py
# pylint --disable=locally-disabled test_release.py

import pytest
from pkgbld.release import release


@pytest.mark.parametrize(
    'rname, pname, version, also37, dryrun',
    [(99, 'taxcalc', '0.23.0', False, False),
     ("Tax-Calculator", 99, '0.23.0', False, False),
     ("Tax-Calculator", 'taxcalc', 99, False, False),
     ("Tax-Calculator", 'taxcalc', '0.23', False, False),
     ("Tax-Calculator", 'taxcalc', '0.23.0rc1', False, False),
     ("Tax-Calculator", 'taxcalc', '0.23.0', list(), False),
     ("Tax-Calculator", 'taxcalc', '0.23.0', False, list())]
)
def test_improper_release_calls(rname, pname, version, also37, dryrun):
    """
    Test release calls with parameters that generate a ValueError.
    """
    with pytest.raises(ValueError):
        release(rname, pname, version, also37, dryrun)
