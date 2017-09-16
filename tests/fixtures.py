import os
import pytest

import seafileapi
from tests.utils import randstring
from seafileapi.admin import Account

SERVER = os.environ.get('SEAFILE_TEST_SERVER_ADDRESS', 'http://address:8000')
USER = os.environ.get('SEAFILE_TEST_USERNAME', 'test@stest.com')
PASSWORD = os.environ.get('SEAFILE_TEST_PASSWORD', 'password')
ADMIN_USER = os.environ.get('SEAFILE_TEST_ADMIN_USERNAME', 'admin@test.com')
ADMIN_PASSWORD = os.environ.get('SEAFILE_TEST_ADMIN_PASSWORD', 'password')

print(os.environ.items())
@pytest.fixture(scope='session')
def client():
    return seafileapi.connect(SERVER, USER, PASSWORD)


@pytest.fixture(scope='session')
def Account():
    return seafileapi.admin.Account


@pytest.yield_fixture(scope='function')
def repo(client):
    repo_name = 'tmp-测试资料库-%s' % randstring()
    repo_desc = 'tmp, 一个测试资料库-%s' % randstring()
    repo = client.repos.create_repo(repo_name, repo_desc)
    try:
        yield repo
    finally:
        repo.delete()


@pytest.yield_fixture(scope='function')
def group(client):
    group_name = randstring()
    group = client.groups.add_group(group_name)
    try:
        yield group
    finally:
        group.delete()

@pytest.yield_fixture(scope='function')
def test_account1(client):
    test_account = client.admin.create_account('{}@test.com'.format(randstring(6)), randstring(6))
    try:
        yield test_account
    finally:
        test_account.delete()

@pytest.yield_fixture(scope='function')
def test_account2(client):
    test_account = client.admin.create_account('{}@test.com'.format(randstring(6)), randstring(6))
    try:
        yield test_account
    finally:
        test_account.delete()