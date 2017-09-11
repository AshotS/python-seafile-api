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
        self.client.delete('/api/v2.1/groups/{}/members/{}/'.format(self.id, self.name))

    def delete(self):
        self.client.delete(self.GROUPS_URL.format(self.id))

    def rename(self, new_name):
        self.client.put(self.GROUPS_URL.format(self.id), data={'name': new_name})
        self.name = new_name

    def transfer(self, new_owner):
        self.client.put(self.GROUPS_URL.format(self.id), data={'owner': new_owner})
        self.owner = new_owner
