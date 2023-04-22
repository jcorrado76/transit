import abc


class IConnection(abc.ABC):
    """
    Abstract base class for Connections.
    """
    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError('Need to implement the connect method')

    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError('Need to implement the disconnect method')
