import sys
import os
import envy

from envy import active_venv, get_active_venv, in_python_package, get_package_name, get_envy_path, get_venv_package_path, original_backed_up, helper

from mock import MagicMock
from mock import patch

base = os.getcwd()

def setup_test(f):
    @patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
    @patch('envy.helper.get_py_version', return_value='2.7')
    @patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
    def wrap_patches(*args, **kwargs):
        return f(*args, **kwargs)

    return wrap_patches

@setup_test
def test_is_active_venv(mock_prefix, mock_version, mock_os):
    assert active_venv() == True

@setup_test
def test_get_package_name(mock_prefix, mock_version, mock_os):
    assert get_package_name() == 'some_package'

@setup_test
def test_get_active_venv(mock_prefix, mock_version, mock_os):
    assert envy.get_active_venv() == 'someenv'

@setup_test
def test_in_python_package(mock_prefix, mock_version, mock_os):
    assert in_python_package() == True

@setup_test
@patch('os.path.expanduser', return_value='./testsrc/someuser/.envies/someenv/some_package')
def test_get_envy_path(mock_prefix, mock_version, dummy, mock_os):
    assert get_envy_path() == './testsrc/someuser/.envies/someenv/some_package'

@setup_test
@patch('os.path.expanduser', return_value='{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))
def test_get_package_name(mock_prefix, mock_version, dummy, mock_os):
    assert get_venv_package_path() == '{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base)

@setup_test
def test_in_python_package_nested_case(mock_prefix, mock_version, mock_os):
    assert in_python_package() == True
