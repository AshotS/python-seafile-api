class StarredFiles:
    STARRED_FILES_URL = '/api2/starredfiles/'

    def __init__(self, client):
        self.client = client

    def list_files(self):
        return self.client.get(self.STARRED_FILES_URL).json()

    def star_file(self, repo_id, path):
        self.client.post(self.STARRED_FILES_URL, data={'repo_id': repo_id, 'p': path})

    def unstar_file(self, repo_id, path):
        self.client.delete(self.STARRED_FILES_URL + '?repo_id={}&p={}'.format(repo_id, path))
