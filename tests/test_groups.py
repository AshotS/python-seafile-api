import pytest
from seafileapi.utils import randstring


def test_groups(group, client):
    assert group in client.groups.list_groups()
    new_name = randstring(5)
    group.rename(new_name)
    assert group.name == new_name

