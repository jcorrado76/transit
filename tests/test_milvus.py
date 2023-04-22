import pytest
from pymilvus import Collection
from pymilvus.orm.connections import Connections

from transit import milvus


@pytest.fixture(scope='module')
def local_milvus_connections():
    connections = Connections()
    milvus.connect_to_milvus_server(alias='default', host='localhost', port='19530')
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
    milvus.connect_to_milvus_server(host, port, alias)
    assert local_milvus_connections.has_connection(alias=alias)


def test_can_create_collection(local_milvus_connections):
    alias_name = 'default'
    milvus.create_collection(alias_name)
    assert local_milvus_connections.has_connection(alias=alias_name)
