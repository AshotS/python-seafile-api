from seafileapi.utils import raise_does_not_exist, tsstr_sec


class Account:
    __slots__ = (
        'client', 'id', 'email', 'password', 'is_staff',
        'is_active', 'usage', 'storage', 'create_time',
        'department', 'name', 'note', 'ACCOUNT_URL')

    def __init__(self, client, email, **kwargs):
        self.client = client
        self.email = email
        self.ACCOUNT_URL = '/api2/accounts/{}/'.format(self.email)

        account_info = kwargs or self.get_info()

        self.id = account_info.get('id')
        self.password = account_info.get('password')
        self.is_staff = account_info.get('is_staff', False)
        self.is_active = account_info.get('is_active', True)
        self.usage = account_info.get('usage')
        self.storage = int(account_info.get('total', 0))
        self.create_time = tsstr_sec(account_info.get('create_time', 0))
        self.department = account_info.get('department')
        self.name = account_info.get('name')
        self.note = account_info.get('note')

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return 'SeafileAccount<id={}, user={}>'.format(self.id, self.email)

    __repr__ = __str__

    def get_info(self):
        return self.client.get(self.ACCOUNT_URL).json()

    def create(self):
        data = {'password': self.password, 'is_staff': self.is_staff, 'is_active': self.is_active}
        self.client.put(self.ACCOUNT_URL, data=data)

    def update(self):
        data = {'name': self.name, 'is_staff': self.is_staff, 'is_active': self.is_active, 'storage': self.storage}
        if self.password:
            data.update({'password': self.password})
        self.client.put(self.ACCOUNT_URL, data=data)
        self.__init__(self.client, self.email)

    def delete(self):
        self.client.delete(self.ACCOUNT_URL)

    def migrate(self, **kwargs):
        raise NotImplemented

    def set_quota(self, limit):
        self.client.put(self.ACCOUNT_URL, data={'storage': limit})


class SeafileAdmin:
    """Wraps various admin operations to interact with seahub http api.
    """
    ACCOUNTS_URL = '/api2/accounts/'
    SERVER_INFO = '/api2/server-info/'

    def __init__(self, client):
        self.client = client

    def list_accounts(self, start=0, limit=100):
        accounts = self.client.get(self.ACCOUNTS_URL, {'start': start, 'limit': limit}).json()
        return [Account(self.client, email=account['email']) for account in accounts]

    @raise_does_not_exist('The requested account does not exist')
    def get_account(self, email):
        return Account(self.client, email)

    def create_account(self, email, password):
        account = Account(self.client, email, password=password)
        account.create()
        return account

    def server_info(self):
        return self.client.get(self.SERVER_INFO).json()
