import pytest
from evolution.ab_testing import ABTesting

def test_ab_testing():
    ab = ABTesting()
    ab.create_experiment()
    assert True
