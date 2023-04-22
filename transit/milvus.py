"""
Implementation of the repository pattern for Milvus, the vector database.
"""
import pymilvus
import requests
from loguru import logger
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

# 19530 is for gRPC, which is the default when you connect
# to a Milvus server with Milvus SDKs
# 9091 is for the RESTful API, which is used when you connect
# to a Milvus server with an HTTP client
ALLOWED_PORTS = set([19530, 9091])

def milvus_server_is_running(url='http://localhost:9091/api/v1/health'):
    """
    Tests if the Milvus server is running.
    """
    logger.info(f'Testing if Milvus server is running at {url}...')
    response = requests.get(url)
    logger.info(f'Received response status code: {response.status_code}')
    return response.status_code == 200



def connect_to_milvus_server(host, port, alias='default'):
    """
    Connect to a Milvus server via the gRPC protocol.
    """
    if milvus_server_is_running():
        logger.info(f'Connecting to Milvus server at {host}:{port}...')
        milvus_connection = connections.connect(
            alias=alias,
            host=host,
            port=port,
        )
    return milvus_connection


def create_collection(alias):
    fields = [
        FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name='random', dtype=DataType.DOUBLE),
        FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=8)
    ]
    schema = CollectionSchema(fields, 'hello_milvus is the simplest demo to introduce the APIs')
    hello_milvus = Collection(alias, schema)
