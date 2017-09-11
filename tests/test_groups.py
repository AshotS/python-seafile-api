import pytest
from seafileapi.utils import randstring


@pytest.mark.parametrize('group_name', [randstring(6)])
def test_groups(client, group_name):
    test_group = client.groups.add_group(group_name)
    assert test_group in client.groups.list_groups()
    new_name = randstring(5)
    test_group.rename(new_name)
    assert test_group.name == new_name
    test_group.delete()
    assert test_group not in client.groups.list_groups()