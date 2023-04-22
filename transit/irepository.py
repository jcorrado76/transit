"""
Abstract base class for all implementations of repository patterns.
"""
import abc


class IRepository(abc.ABC):
    """
    Abstract base class for Repository implementations.
    """
    @abc.abstractmethod
    def get(self):
        raise NotImplementedError('Need to implement the get method')

    @abc.abstractmethod
    def insert(self):
        raise NotImplementedError('Need to implement the insert method')

    @abc.abstractmethod
    def upsert(self):
        raise NotImplementedError('Need to implement the upsert method')


    @abc.abstractmethod
    def delete(self):
        raise NotImplementedError('Need to implement the delete method')
