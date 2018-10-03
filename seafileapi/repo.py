from urllib import parse

from seafileapi.files import SeafDir, SeafFile
from seafileapi.utils import raise_does_not_exist


class Repo:
    """
    A seafile library
    """
    __slots__ = ('client', 'id', 'name', 'desc', 'encrypted', 'owner', 'perm')

    def __init__(self, client, repo_id, repo_name, repo_desc,
                 encrypted, owner, perm):
        self.client = client
        self.id = repo_id
        self.name = repo_name
        self.desc = repo_desc
        self.encrypted = encrypted
        self.owner = owner
        self.perm = perm

    def __str__(self):
        return 'SefileRepo<id={}, name={}>'.format(self.id, self.name)

    __repr__ = __str__

    @classmethod
    def from_json(cls, client, repo_json):
        """

        :param client:
        :param repo_json:
        :return:
        """
        repo_id = repo_json['id']
        repo_name = repo_json['name']
        repo_desc = repo_json.get('desc', '')
        encrypted = repo_json['encrypted']
        perm = repo_json['permission']
        owner = repo_json['owner']

        return cls(client, repo_id, repo_name, repo_desc, encrypted, owner, perm)

    def is_readonly(self):
        """

        :return:
        """
        return 'w' not in self.perm

    @raise_does_not_exist('The requested file does not exist')
    def get_file(self, path):
        """Get the file object located in `path` in this repo.

        Return a :class:`SeafFile` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/file/detail/' % self.id
        query = '?' + parse.urlencode(dict(p=path))
        file_json = self.client.get(url + query).json()

        return SeafFile(self, path, file_json['id'], file_json['size'])

    @raise_does_not_exist('The requested dir does not exist')
    def get_dir(self, path):
        """Get the dir object located in `path` in this repo.

        Return a :class:`SeafDir` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/dir/' % self.id
        query = '?' + parse.urlencode(dict(p=path))
        resp = self.client.get(url + query)
        dir_id = resp.headers['oid']
        dir_json = resp.json()
        directory = SeafDir(self, path, dir_id)
        directory.load_entries(dir_json)
        return directory

    def delete(self):
        """Remove this repo. Only the repo owner can do this"""
        self.client.delete('/api2/repos/' + self.id)

    def list_revisions(self):
        """List the history of this repo

        Returns a list of :class:`RepoRevision` object.
        """
        res = self.client.get('/api/v2.1/repos/{}/history/'.format(self.id)).json()
        return [RepoRevision(self.client, self, **repo) for repo in res['data']]

    # Operations only the repo owner can do:

    def update(self, name=None, desc=None):
        """Update the name and/or description of this repo. Only the repo owner can do
        this.
        """
        pass

    def get_settings(self):
        """Get the settings of this repo. Returns a dict containing the following
        keys:

        `history_limit`: How many days of repo history to keep.
        """
        pass

    def revert(self, commit_id):
        """

        :param commit_id:
        """
        pass


class RepoRevision:
    """

    """
    __slots__ = ('client', 'repo', 'commit_id', 'time')

    def __init__(self, client, repo, **kwargs):
        self.client = client
        self.repo = repo
        self.commit_id = kwargs.get('commit_id')
        self.time = kwargs.get('time')

    def __str__(self):
        return 'SefileRepoRevision<repo={}, commit_id={}>'.format(self.repo, self.commit_id)

    __repr__ = __str__

    def restore(self):
        """Restore the repo to this revision"""
        self.repo.revert(self.commit_id)
