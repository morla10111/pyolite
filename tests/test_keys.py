from unittest import TestCase

from mock import patch, MagicMock, call
from nose.tools import eq_

from pyolite.keys import ListKeys


class TestKeyList(TestCase):
  def test_if_we_commit_after_a_key_append(self):
    key_path = "tests/fixtures/simple_key.pub"

    mock_file = MagicMock()
    mock_file.__str__ = lambda x: key_path
    mock_path = MagicMock(return_value=mock_file)

    mock_hashlib = MagicMock()
    mock_hashlib.md5.hexdigest.return_value = "HASH"

    mock_user = MagicMock()
    mock_user.path = "path"
    mock_user.name = "test"

    with patch.multiple('pyolite.keys', Path=mock_path,
                        hashlib=mock_hashlib):
      keys = ListKeys(mock_user)

      keys.append(key_path)

    mock_path.has_calls([
        call("path", key_path),
        call("path", "keydir", "HASH"),
        call(mock_file, "test"),
    ])

    eq_(mock_file.isfile.call_count, 1)
    eq_(mock_file.mkdir.call_count, 1)
    mock_file.write_file.assert_called_once_with('nothing to see here\n')
