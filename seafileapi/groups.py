import json


class Groups:
    GROUPS_URL = '/api/v2.1/groups/{}/'

    def __init__(self, client):
        self.client = client

    def get_group(self, id):
        res = self.client.get(self.GROUPS_URL.format(id)).json()
        return Group(self.client, **res)

    def add_group(self, name):
        res = self.client.post(self.GROUPS_URL.format(''), data={'name': name}).json()
        return self.get_group(res['id'])

    def list_groups(self):
        groups = self.client.get(self.GROUPS_URL.format('')).json()
        return [Group(self.client, **group) for group in groups] if groups else []


class Group:
    GROUPS_URL = '/api/v2.1/groups/{}/'
    GROUP_MEMBERS_URL = '/api/v2.1/groups/{}/{}'
    GROUP_MESSAGES_URL = '/api/v2.1/groups/{}/discussions/{}'
    __slots__ = ('client', 'id', 'name', 'owner', 'created_at', 'admins', 'avatar_url', 'wiki_enabled')

    def __init__(self, client, **kwargs):
        self.client = client
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.owner = kwargs.get('owner')
        self.created_at = kwargs.get('created_at')
        self.avatar_url = kwargs.get('avatar_url')
        self.wiki_enabled = kwargs.get('wiki_enabled')
        self.admins = kwargs.get('admins')

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return 'SeafileGroup<id={}, name={}>'.format(self.id, self.name)

    __repr__ = __str__

    def quit(self):
        self.client.delete(self.GROUP_MEMBERS_URL.format(self.id, self.client.username))

    def delete(self):
        self.client.delete(self.GROUPS_URL.format(self.id))

    def rename(self, new_name):
        self.client.put(self.GROUPS_URL.format(self.id), data={'name': new_name})
        self.name = new_name

    def transfer(self, new_owner):
        self.client.put(self.GROUPS_URL.format(self.id), data={'owner': new_owner})
        self.owner = new_owner

    def get_member(self, email):
        res = self.client.get(self.GROUP_MEMBERS_URL.format(self.id, email)).json()
        return Member(self.client, self.id, **res)

    def list_members(self):
        members = self.client.get(self.GROUP_MEMBERS_URL.format(self.id, '')).json()
        return [Member(self.client, self.id, **member) for member in members] if members else []

    def add_member(self, email):
        res = self.client.post(self.GROUP_MEMBERS_URL.format(self.id, ''), data={'email': email}).json()
        return self.get_member(res['email'])

    def list_messages(self):
        messages = self.client.get(self.GROUP_MESSAGES_URL.format(self.id, '')).json()
        return [Message(self.client, **message) for message in messages] if messages else []

    def send_message(self, content):
        res = self.client.post(self.GROUP_MESSAGES_URL.format(self.id, ''), data={'content': content}).json()
        return Message(self.client, **res)

class Member:
    GROUP_MEMBERS_URL = '/api/v2.1/groups/{}/{}'
    __slots__ = ('client', 'group_id', 'login_id', 'name', 'avatar_url', 'is_admin', 'contact_email', 'email')

    def __init__(self, client, group_id, **kwargs):
        self.client = client
        self.group_id = group_id
        self.login_id = kwargs.get('login_id')
        self.name = kwargs.get('name')
        self.avatar_url = kwargs.get('avatar_url')
        self.is_admin = kwargs.get('is_admin', False)
        self.contact_email = kwargs.get('contact_email')
        self.email = kwargs.get('email')

    def __eq__(self, other):
        return self.login_id == other.login_id

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.login_id)

    def __str__(self):
        return 'SeafileGropMember<id={}, name={}>'.format(self.login_id, self.name)

    __repr__ = __str__

    def delete(self):
        self.client.delete(self.GROUP_MEMBERS_URL.format(self.group_id, self.email))

    def set_admin(self):
        if not self.is_admin:
            self.client.put(self.GROUP_MEMBERS_URL.format(self.group_id, ''), data={'is_admin': 'true'})
            self.is_admin = True

    def unset_admin(self):
        if self.is_admin:
            self.client.put(self.GROUP_MEMBERS_URL.format(self.group_id, ''), data={'is_admin': 'false'})
            self.is_admin = False


class Message:
    GROUP_MESSAGES_URL = '/api/v2.1/groups/{}/discussions/{}'
    __slots__ = ('client', 'group_id', 'content', 'created_at', 'avatar_url',
                 'id', 'user_email', 'user_login_id', 'user_name')

    def __init__(self, client, **kwargs):
        self.client = client
        self.group_id = kwargs.get('group_id')
        self.id = kwargs.get('id')
        self.user_name = kwargs.get('user_name')
        self.avatar_url = kwargs.get('avatar_url')
        self.content = kwargs.get('content')
        self.created_at = kwargs.get('created_at')
        self.user_email = kwargs.get('user_email')
        self.user_login_id = kwargs.get('user_login_id')

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return 'SeafileGropMessage<id={}, user_name={}>'.format(self.id, self.user_name)

    __repr__ = __str__

    def delete(self):
        self.client.delete(self.GROUP_MESSAGES_URL.format(self.group_id, self.id))
