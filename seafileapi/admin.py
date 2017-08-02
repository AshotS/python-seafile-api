from seafileapi.utils import raise_does_not_exist, tsstr_sec


class Account:
    def __init__(self, client, email, **kwargs):
        self.client = client
        self.email = email
        self.ACCOUNT_URL = '/api2/accounts/{}/'.format(self.email)

        account_info = kwargs or self.get_info()

        self.id = account_info.get('id', None)
        self.password = account_info.get('password', None)
        self.is_staff = account_info.get('is_staff', False)
        self.is_active = account_info.get('is_active', True)
        self.usage = account_info.get('usage', None)
        self.storage = int(account_info.get('total', 0))
        self.create_time = tsstr_sec(account_info.get('create_time', 0))
        self.department = account_info.get('department', None)
        self.name = account_info.get('name', None)
        self.note = account_info.get('note', None)

    def get_info(self):
        return self.client.get(self.ACCOUNT_URL.format(self.email)).json()

    def create(self):
        data = {'password': self.password, 'is_staff': self.is_staff, 'is_active': self.is_active}
        self.client.put(self.ACCOUNT_URL, data=data)

    def update(self):
        data = {'name': self.name, 'is_staff': self.is_staff, 'is_active': self.is_active, 'storage': self.storage}
        if self.password:
            data.update({'password': self.password})
        self.client.put(self.ACCOUNT_URL, data=data)

    def delete(self):
        self.client.delete(self.ACCOUNT_URL)

    def migrate(self, **kwargs):
        pass

    def set_quota(self, limit):
        self.client.put(self.ACCOUNT_URL, data={'storage': limit})


class SeafileAdmin:
    """Wraps various admin operations to interact with seahub http api.
    """
    ACCOUNTS_URL = '/api2/accounts/'
    SERVER_INFO = '/api2/server-info/'

    def __init__(self, client):
        self.client = client

    def lists_accounts(self, limit=100):
        return self.client.get(self.ACCOUNTS_URL, {'start': 0, 'limit': limit}).json()

    @raise_does_not_exist('The requested account does not exist')
    def get_account(self, email):
        return Account(email, self.client)

    def create_account(self, email, password):
        account = Account(self.client, email, password=password)
        account.create()
        return account

    def server_info(self):
        return self.client.get(self.SERVER_INFO).json()
