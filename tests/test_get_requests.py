import hashlib
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import Mock

from syncr_tracker.tracker import handle_get


def test_handle_get():
    h = hashlib.sha256(b'foobar')
    node_id = h.digest()

    i = hashlib.sha256(b'biaazquxx')
    drop_id = h.digest() + i.digest()

    conn = Mock()
    conn.send = MagicMock()
    with mock.patch(
        'syncr_tracker.tracker.retrieve_drop_info', autospec=True,
    ) as mock_retrieve_drop_info, mock.patch(
        'syncr_tracker.tracker.retrieve_public_key', autospec=True,
    ) as mock_retrieve_public_key, mock.patch(
        'syncr_tracker.tracker.send_server_response', autospec=True,
    ) as mock_send_server_response:

        request = ['GET', node_id, None]
        handle_get(conn, request)
        mock_retrieve_public_key.assert_called_once()
        mock_retrieve_drop_info.assert_not_called()
        mock_send_server_response.assert_not_called()

        request = ['GET', drop_id, None]
        handle_get(conn, request)
        mock_retrieve_drop_info.assert_called_once()
        mock_retrieve_public_key.assert_not_called()
        mock_send_server_response.assert_not_called()

        request = ['GET', b'\00', None]
        handle_get(conn, request)
        mock_retrieve_drop_info.assert_called_once()
        mock_retrieve_public_key.assert_called_once()
        mock_send_server_response.assert_called_once()
