import pytest

from tests.utils import randstring


def test_accounts_list(client):
    accounts = client.admin.lists_accounts()
    print(accounts)
    assert len(accounts) > 0


def test_server_info(client):
    info = client.admin.server_info()
    assert 'version' in info


@pytest.mark.parametrize('password', [randstring(6)])
@pytest.mark.parametrize('name', [randstring(6)])
@pytest.mark.parametrize('email', ['qwerty@asdf.com'])
def test_cud_account(client, email, password, Account, name):
    # create account
    test_account = client.admin.create_account(email, password)
    assert isinstance(test_account, Account)

    # upadte account fields
    size = 100
    test_account.name = name
    test_account.is_staff = True
    test_account.is_active = True
    test_account.storage = size
    test_account.update()
    assert test_account.name == name
    assert test_account.storage == size * 1000000

    # delete account
    test_account.delete()
    assert test_account.email not in [i['email'] for i in client.admin.lists_accounts()]
