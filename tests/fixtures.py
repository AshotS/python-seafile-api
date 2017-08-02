import os
import pytest

import seafileapi
from tests.utils import randstring

SERVER = os.environ.get('SEAFILE_TEST_SERVER_ADDRESS', 'http://cloud.vault:8000')
USER = os.environ.get('SEAFILE_TEST_USERNAME', 'sdsd@sdfsds.ru')
PASSWORD = os.environ.get('SEAFILE_TEST_PASSWORD', '4368906oo')
ADMIN_USER = os.environ.get('SEAFILE_TEST_ADMIN_USERNAME', 'sdsd@sdfsds.ru')
ADMIN_PASSWORD = os.environ.get('SEAFILE_TEST_ADMIN_PASSWORD', '4368906oo')


@pytest.fixture(scope='session')
def client():
    return seafileapi.connect(SERVER, USER, PASSWORD)


@pytest.yield_fixture(scope='function')
def repo(client):
    repo_name = 'tmp-测试资料库-%s' % randstring()
    repo_desc = 'tmp, 一个测试资料库-%s' % randstring()
    repo = client.repos.create_repo(repo_name, repo_desc)
    try:
        yield repo
    finally:
        repo.delete()
