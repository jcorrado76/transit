"""
Implementation of the repository pattern for Milvus, the vector database.
"""
import asyncio
import os

import httpx
import pymilvus
import requests
from loguru import logger
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)
from pymilvus.orm.connections import Connections

from transit import iconnection, irepository

# 19530 is for gRPC, which is the default when you connect
# to a Milvus server with Milvus SDKs
# 9091 is for the RESTful API, which is used when you connect
# to a Milvus server with an HTTP client
ALLOWED_PORTS = set([19530, 9091])





class FakeMilvusConnection(iconnection.IConnection):
    def __init__(self, alias=None, host=None, port=None):
        pass

    def connect(self):
        logger.info('Connected to FakeMilvusConnection')

    def disconnect(self):
        logger.info('Disconnected from FakeMilvusConnection')

    @classmethod
    def local_connection(cls, alias, host, port):
        return cls(alias=alias, host=host, port=port)

class MilvusConnection(iconnection.IConnection):
    def __init__(self, alias=None, host=None, port=None):
        pass

    def connect(self):
        print('Connected to FakeMilvusConnection')

    def disconnect(self):
        print('Disconnected from FakeMilvusConnection')

    @classmethod
    def local_connection(cls, alias, host, port):
        return cls(alias=alias, host=host, port=port)



class FakeMilvusCollection(iconnection.IConnection):
    def connect(self):
        logger.info('Connected to FakeMilvusCollection')

    def disconnect(self):
        logger.info('Disconnected from FakeMilvusCollection')




class MilvusRepository(irepository.IRepository):
    def __init__(self, alias=None, uri=None, user=None, password=None, collection_name=None, openai_api_key=None):
        self.alias = alias or 'default'
        self.uri = uri or os.environ.get('MILVUS_DB_URI')
        self.user = user or os.environ.get('MILVUS_DB_USER')
        self.password = password or os.environ.get('MILVUS_DB_PASSWORD')
        self.collection_name = collection_name or os.environ.get('MILVUS_COLLECTION_NAME')
        self.openai_api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')

    def __enter__(self):
        pass
        # if 'localhost' in self.uri:
        #     connections.connect("default", host="localhost", port="19530")
        # else:
        #     connections.connect(alias=self.alias, uri=self.uri, user=self.user, password=self.password, secure=True)
        # openai.api_key = self.openai_api_key

        # self.collection = Collection(name=self.collection_name)
        # self.collection.load()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
        # connections.disconnect(self.alias)
        # print("closing milvus connection")

    def get(self):
        pass

    def insert(self):
        pass

    def upsert(self):
        pass

    def delete(self):
        pass

    # async def create_embedding(self, text):
    #     async with httpx.AsyncClient() as client:
    #         url = f'https://api.openai.com/v1/engines/text-embedding-ada-002/embed'
    #         headers = {
    #             'Authorization': f'Bearer {self.openai_api_key}',
    #             'Content-Type': 'application/json'
    #         }
    #         data = {'input': text}
    #         response = await client.post(url, json=data, headers=headers)

    #     return response.json()['data'][0]['embedding']

    # async def insert_data(self, text_chunks):
    #     ids = []
    #     embeddings_to_insert = []
    #     bill_ids = []

    #     tasks = [self.create_embedding(text) for text in text_chunks]
    #     embeddings = await asyncio.gather(*tasks)

    #     for idx, embedding in enumerate(embeddings):
    #         ids.append(f'test_{idx}')
    #         embeddings_to_insert.append(embedding)
    #         bill_ids.append('test_bill_id')

    #     self.collection.insert(data=[
    #         ids,
    #         embeddings_to_insert,
    #         bill_ids,
    #     ])

    #     return ids

    # async def search(self, query_text, top_k=10):
    #     query_embedding = await self.create_embedding(query_text)

    #     search_params = {'metric_type': 'L2', 'params': {'nprobe': 10}}
    #     results = self.collection.search(
    #         data=[query_embedding],
    #         anns_field='embedding',
    #         param=search_params,
    #         limit=top_k
    #     )

    #     return results

    # def delete_data(self, ids):
    #     for inserted_id in ids:
    #         self.collection.delete(expr=f"id in ['{inserted_id}']")

    @staticmethod
    def local_milvus_server_is_running(url='http://localhost:9091/api/v1/health'):
        """
        Tests if a local Milvus server is running.
        """
        logger.info(f'Testing if a local Milvus server is running at {url}...')
        response = requests.get(url)
        logger.info(f'Received response status code: {response.status_code}')
        return response.status_code == 200


    @staticmethod
    def connect_to_milvus_server(host, port, alias='default'):
        """
        Connect to a Milvus server via the gRPC protocol.
        """
        if MilvusRepository.local_milvus_server_is_running():
            logger.info(f'Connecting to Milvus server at {host}:{port}...')
            milvus_connection = connections.connect(
                alias=alias,
                host=host,
                port=port,
            )
        return milvus_connection

    @staticmethod
    def create_collection(alias):
        fields = [
            FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=False),
            FieldSchema(name='random', dtype=DataType.DOUBLE),
            FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=8)
        ]
        schema = CollectionSchema(fields, 'hello_milvus is the simplest demo to introduce the APIs')
        hello_milvus = Collection(alias, schema)

    @staticmethod
    def get_connections():
        """
        This returns a handle to the pymilvus Singleton Connections object.
        """
        return Connections()

    @staticmethod
    def assert_connection_exists(alias):
        assert MilvusRepository.get_connections().has_connection(alias=alias), f'Connection {alias} does not exist.'

def milvus_factory():
    pass
