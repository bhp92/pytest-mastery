import pytest
import source

def test_warn():
    with pytest.warns(DeprecationWarning, match="addition"):
        source.operation(2,3)