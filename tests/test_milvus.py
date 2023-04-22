import pytest
from pymilvus import Collection
from pymilvus.orm.connections import Connections

from transit import milvus


@pytest.fixture(scope='module')
def local_milvus_connections():
    connections = Connections()
    milvus.MilvusRepository.connect_to_milvus_server(alias='default', host='localhost', port='19530')
    return connections



def test_allowed_ports():
    """
    Ports are defined here:
    https://milvus.io/docs/manage_connection.md#Manage-Milvus-Connections
    """
    assert milvus.ALLOWED_PORTS == set([19530, 9091])



def test_can_connect_to_local_milvus_server(local_milvus_connections):
    host='localhost'
    port='19530'
    alias='default'
    milvus.MilvusRepository.connect_to_milvus_server(host, port, alias)
    assert local_milvus_connections.has_connection(alias=alias)


def test_can_create_collection(local_milvus_connections):
    alias_name = 'default'
    milvus.MilvusRepository.create_collection(alias_name)
    assert local_milvus_connections.has_connection(alias=alias_name)

def test_can_instantiate_fake_milvus_connection():
    connection = milvus.FakeMilvusConnection()

def test_can_connect_and_disconnect_fake_milvus_collection():
    connection = milvus.FakeMilvusConnection()
    connection.connect()

    connection.disconnect()

def test_can_get_connections(local_milvus_connections):
    connections = milvus.MilvusRepository.get_connections()
    assert connections.has_connection('default')

def test_can_assert_connection_exists(local_milvus_connections):
    milvus.MilvusRepository.assert_connection_exists('default')

def test_can_instantiate_local_fake_milvus_connection():
    connection = milvus.FakeMilvusConnection.local_connection(
        'default',
        host='localhost',
        port='19530'
    )
    assert connection is not None


def test_can_instantiate_milvus_repository():
    milvus_repository = milvus.MilvusRepository()

def test_can_instantiate_milvus_with_context_manager():
    with milvus.MilvusRepository() as repository:
        assert repository is not None
