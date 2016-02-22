import sys
import os
import envy

from envy import active_venv, get_active_venv, in_python_package, get_package_name, get_envy_path, get_venv_package_path, original_backed_up, helper

from mock import MagicMock
from mock import patch

base = os.getcwd()

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_is_active_venv(mock_prefix, mock_version, mock_os):
    assert active_venv() == True

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_get_package_name(mock_prefix, mock_version, mock_os):
    assert get_package_name() == 'some_package'

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_get_active_venv( mock_prefix, mock_version, mock_os):
    assert envy.get_active_venv() == 'someenv'

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_in_python_package(mock_prefix, mock_version, mock_os):
    assert in_python_package() == True

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('os.path.expanduser', return_value='./testsrc/someuser/.envies/someenv/some_package')
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_get_envy_path(mock_prefix, mock_version, dummy, mock_os):
    assert get_envy_path() == './testsrc/someuser/.envies/someenv/some_package'

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('os.path.expanduser', return_value='{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))
@patch('envy.helper.get_py_version', return_value='2.7')
@patch('envy.helper.get_sys_prefix', return_value="./testsrc/someuser/.virtualenvs/someenv/bin")
def test_get_package_name(mock_prefix, mock_version, dummy, mock_os):
    assert get_venv_package_path() == '{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base)

# # def test_in_python_package_nested_case():
# #     mock('os.getcwd', returns='{}/tests/testsrc/someuser/src/some_package/some_package'.format(base))
# #     assert in_python_package() == True
