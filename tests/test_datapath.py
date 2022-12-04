"""
Test datapath module
"""
import pytest
from lib.datapath import DataPath


def test_datapath_getitem():
    "Test DataPath.__getitem__."
    data = {"a": {"b": 1, "c": [2], "d": [[3, 4], [5]]}}
    d = DataPath(data)
    assert d.data is data
    assert d["a"] == {"b": 1, "c": [2], "d": [[3, 4], [5]]}
    assert d["a.b"] == 1
    assert d["a.c"] == [2]
    assert d["a.c.0"] == 2
    assert d["a.c[0]"] == 2
    assert d["a.d"] == [[3, 4], [5]]
    assert d["a.d[0]"] == [3, 4]
    assert d["a.d[0][1]"] == 4
    assert d["a.d[1][0]"] == 5
    with pytest.raises(TypeError):
        _ = d["a.b.c"]
    with pytest.raises(KeyError):
        _ = d["a.e"]
    with pytest.raises(IndexError):
        _ = d["a.c.1"]
    with pytest.raises(IndexError):
        _ = d["a.c[1]"]


def test_datapath_setitem():
    "Test DataPath.__setitem__"
    data = {}
    d = DataPath(data)
    d["a"] = 1
    assert d["a"] == 1


def test_datapath_delitem():
    "Test DataPath.__delitem__"
    data = {"a": 1}
    d = DataPath(data)
    assert d.data is data
    del d["a"]
    assert d.data == {}


def test_datapath_contains():
    "Test DataPath.__contains__"
    data = {"a": 1}
    d = DataPath(data)
    assert "a" in d
    assert "b" not in d
    assert "b.c" not in d


def test_datapath_get():
    "Test DataPath.get"
    data = {"a": 1}
    d = DataPath(data)
    assert d["a"] == 1
    assert d.get("a") == 1
    assert d.get("b") is None
    assert d.get("b", 1) == 1


def test_datapath_repr():
    "Test DataPath.__repr__"
    d = DataPath({})
    assert repr(d) == "DataPath({})"
