import sys
import os
import envy
import pkg_resources

from envy import active_venv, get_active_venv, in_python_package, get_package_name, get_envy_path,  original_backed_up, get_venv_full_package_path

from mock import MagicMock, PropertyMock
from mock import patch

base = os.getcwd()

def setup_test(f):
    @patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
    def wrap_patches(*args, **kwargs):
        with patch('envy.application.sys.prefix', "./testsrc/someuser/.virtualenvs/someenv/bin"):
            with patch('envy.application.imp.find_module', return_value=(None,'{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))):
                with patch.dict('os.environ'):
                    if 'VIRTUAL_ENV' in os.environ:
                        del os.environ['VIRTUAL_ENV']
                    if 'WORKON_HOME' in os.environ:
                        del os.environ['WORKON_HOME']
                    return f(*args, **kwargs)

    return wrap_patches

@setup_test
def test_is_active_venv(mock_os):
    assert active_venv() == True

@setup_test
def test_get_package_name(mock_os):
    assert get_package_name() == 'some_package'

@setup_test
def test_in_python_package(mock_os):
    assert in_python_package() == True

@setup_test
@patch('os.path.expanduser', return_value='./testsrc/someuser/.envies/someenv/some_package')
def test_get_envy_path(dummy, mock_os):
    assert get_envy_path() == './testsrc/someuser/.envies/someenv/some_package'

@setup_test
def test_get_full_package_path(mock_os):
    assert get_venv_full_package_path() == '{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base)

@setup_test
def test_in_python_package_nested_case(mock_os):
    assert in_python_package() == True

@setup_test
def test_get_active_venv_default_case(mock_os):
    assert envy.get_active_venv() == 'someenv'

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
def test_get_active_venv_non_standard_venv_root(mock_os):
    with patch.dict('os.environ', {'VIRTUAL_ENV': 'some_env_root/someenv'}):
        assert get_active_venv() == 'someenv'

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
def test_get_active_venv_using_workon_path(mock_os):
    with patch('envy.application.sys.prefix', "./testsrc/someuser/.envs/someenv/bin"):
        with patch.dict('os.environ', {'WORKON_HOME': '.envs'}):
            if 'VIRTUAL_ENV' in os.environ:
                del os.environ['VIRTUAL_ENV']
            assert get_active_venv() == 'someenv'
