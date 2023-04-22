import pytest

from transit import iconnection


def test_cant_instantiate_abstract_connection():
    with pytest.raises(TypeError):
        connection = iconnection.IConnection()
