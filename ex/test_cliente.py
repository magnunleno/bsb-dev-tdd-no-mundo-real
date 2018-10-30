import json
from unittest.mock import patch, MagicMock
from datetime import date, datetime

import utils


def test_cliente_to_json():
    with patch.object(utils, 'datetime', wraps=utils.datetime) as mock:
        fmt = utils.fmt_datetime(date(2018, 1, 1))
        assert mock.called
        assert mock.call_args[0] == (2018, 1, 1)
        assert len(mock.mock_calls) == 1
        assert fmt == "2018-01-01T00:00:00"

        mock.reset_mock()

        fmt = utils.fmt_datetime(datetime(2018, 1, 1, 2, 3, 4))
        assert not mock.called
        assert fmt == "2018-01-01T02:03:04"


@patch('utils.os.remove', return_value=True)
def test_apaga_arquivo(mock):
    with patch('utils.os.path.exists', return_value=True):
        success = utils.apaga_arquivo('/phony/file')
        assert success

    with patch('utils.os.path.exists', return_value=False):
        success = utils.apaga_arquivo('/phony/file')
        assert not success


def test_cliente_api():
    mock = MagicMock()
    utils.Cliente.use(api=mock)

    mock.fetch.return_value = {"id": 1, "nome": "Fulano"}
    c = utils.Cliente.por_id(1)
    assert mock.fetch.call_count == 1
    assert mock.fetch.call_args[0] == (1,)
    assert c.id == 1
    assert c.nome == "Fulano"

    mock.fetch.reset_mock()
    mock.fetch.return_value = None
    c = utils.Cliente.por_id(3)
    assert c is None
    assert mock.fetch.call_count == 1
    assert mock.fetch.call_args[0] == (3,)
