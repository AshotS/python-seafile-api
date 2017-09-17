from seafileapi.repo import Repo
from seafileapi.utils import raise_does_not_exist


class Repos:
    """

    """
    REPOS_URL = '/api2/repos/'

    def __init__(self, client):
        self.client = client

    def create_repo(self, name, desc=None, password=None):
        """

        :param name:
        :param desc:
        :param password:
        :return:
        """
        data = {'name': name}
        if desc:
            data.update({'desc': desc})
        if password:
            data['passwd'] = password
        repo_json = self.client.post(self.REPOS_URL, data=data).json()
        return self.get_repo(repo_json['repo_id'])

    @raise_does_not_exist('The requested library does not exist')
    def get_repo(self, repo_id):
        """Get the repo which has the id `repo_id`.

        Raises :exc:`DoesNotExist` if no such repo exists.
        """
        repo_json = self.client.get(self.REPOS_URL + repo_id).json()
        return Repo.from_json(self.client, repo_json)

    def list_repos(self):
        """List the repos.

        Return a list of objects of class :class:`Repo`.
        """
        repos_json = self.client.get(self.REPOS_URL).json()
        return [Repo.from_json(self.client, j) for j in repos_json]
