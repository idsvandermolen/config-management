"""
Test datapath module
"""
import pytest
from lib.grafana import generate


def test_dummy():
    "Test dummy."
    assert hasattr(generate, "__doc__")
