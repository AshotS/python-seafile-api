from seafileapi.client import SeafileApiClient


def connect(server, username, password):
    """
    Connect to Seafile server
    :param server: address of the seafile server
    :param username: username
    :param password: password
    :return: :class:`SeafileApiClient`.
    """
    seafile_client = SeafileApiClient(server, username, password)
    return seafile_client
