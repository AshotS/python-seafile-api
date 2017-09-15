import pytest


def test_starred(client):
    assert isinstance(client.starredfiles.list_files(), list)
