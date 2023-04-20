from unittest import mock

import pytest


@pytest.fixture
def ipfs_client():
    """Return an ipfshttpclient.Client mock.
    Used for instantation of :class:`ipfs_storage.InterPlanetaryFileSystemStorage`.
    Introduce it in tests as a function argument `ipfs_client`.
    """
    with (
        mock.patch("ipfs_storage.storage.ipfshttpclient.connect") as ipfs_conn_mock,
        mock.patch("ipfs_storage.storage.ipfshttpclient.Client") as client_mock,
    ):
        ipfs_conn_mock.return_value = client_mock
        yield client_mock
