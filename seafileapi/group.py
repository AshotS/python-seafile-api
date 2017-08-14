class Group:
    GROUP_MEMBERS_URL = '/api2/groups/{}/members/'
    GROUP_MESSAGES_URL = '/api2/group/msgs/{}/'

    def __init__(self, client, group_id, group_name):
        self.client = client
        self.group_id = group_id
        self.group_name = group_name

    def __str__(self):
        return 'SeafileGroup[id={}, name={}]'.format(self.group_id, self.group_name)

    __repr__ = __str__

    def list_memebers(self):
        return self.client.get()

    def delete(self):
        pass

    def add_member(self, username):
        pass

    def remove_member(self, username):
        pass

    def list_group_repos(self):
        pass
