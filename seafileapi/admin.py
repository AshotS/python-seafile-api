from seafileapi.utils import raise_does_not_exist, tsstr_sec


class Account(object):
    __slots__ = (
        'client', 'id', 'email', 'password', 'is_staff',
        'is_active', 'usage', 'total', 'create_time',
        'department', 'name', 'note', 'ACCOUNT_URL')

    def __init__(self, client, email, **account_info):
        self.client = client
        self.email = email
        self.ACCOUNT_URL = '/api2/accounts/{}/'.format(email)

        self.id = account_info.get('id')
        self.password = account_info.get('password')
        self.is_staff = account_info.get('is_staff')
        self.is_active = account_info.get('is_active')
        self.usage = account_info.get('usage')
        self.total = account_info.get('total')
        self.create_time = account_info.get('create_time')
        self.department = account_info.get('department')
        self.name = account_info.get('name')
        self.note = account_info.get('note')

    def __getattribute__(self, item):
        items = (
            'id', 'is_staff',
            'is_active', 'usage', 'total', 'create_time',
            'department', 'name', 'note',)
        if item in items:
            attr = object.__getattribute__(self, item)
            if attr is None:
                self._update_info()
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        items = (
            'password', 'is_staff', 'is_active',
            'name', 'note', 'storage',)
        if key in items and value:

            self.client.put(self.ACCOUNT_URL, data={key: value})
        object.__setattr__(self, key, value)

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.email)

    def __str__(self):
        return 'SeafileAccount<id={}, user={}>'.format(self.id, self.email)

    __repr__ = __str__

    def _update_info(self):
        account_info = self.get_info()
        account_info.pop('email', None)
        self.__init__(self.client, self.email, **account_info)

    @property
    def total_usage(self):
        return int(self.total)

    @property
    def created(self):
        return tsstr_sec(self.create_time)

    @raise_does_not_exist('The requested account does not exist')
    def get_info(self):
        return self.client.get(self.ACCOUNT_URL).json()

    def create(self):
        data = {'password': self.password, 'is_staff': self.is_staff or False, 'is_active': self.is_active or True}
        self.client.put(self.ACCOUNT_URL, data=data)

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

    def list_accounts(self, start=0, limit=100, scope=None):
        """
        Return a list of :class:`Account` objects. To retrieve all users, just set both start and limit to -1.
        :param start: (default to 0)
        :param limit: (default to 100)
        :param scope: (default None, accepted values: 'LDAP' or 'DB' or 'LDAPImport')
        :return:
        """
        accounts = self.client.get(self.ACCOUNTS_URL, params={'start': start, 'limit': limit, 'scope': scope}).json()
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
