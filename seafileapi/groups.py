from seafileapi.group import Group


class Groups:
    GROUPS_URL = '/api2/groups/{}/'

    def __init__(self, client):
        self.client = client

    def add_group(self, name):
        self.client.put(self.GROUPS_URL.format(''), data={'group_name': name})

    def delete_group(self, id):
        self.client.delete(self.GROUPS_URL.format(id))

    def rename_group(self, id, new_name):
        self.client.post(self.GROUPS_URL.format(id), data={'operation': 'rename', 'group_name': new_name})

    def list_groups(self):
        return self.client.get(self.GROUPS_URL.format('')).json()
