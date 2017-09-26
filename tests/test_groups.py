import pytest
from seafileapi.utils import randstring


def test_groups(group, client):
    assert group in client.groups.list_groups()

    group1 = client.groups.get_group(group.id)
    assert group == group1

    new_name = randstring(5)
    group.rename(new_name)

    assert group.name == new_name


def test_members(group, test_account1, test_account2):
    member1 = group.add_member(test_account1.email)
    member2 = group.add_member(test_account2.email)
    assert member1 in group.list_members()

    member1.set_admin()
    assert member1.is_admin
    member1.unset_admin()
    assert not member1.is_admin

    member2.delete()
    assert member2 not in group.list_members()


def test_messages(group, test_account1, test_account2):
    member1 = group.add_member(test_account1.email)
    member2 = group.add_member(test_account2.email)

