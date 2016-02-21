import sys
import os

from envy import active_venv, get_active_venv, in_python_package, get_package_name, get_envy_path, get_venv_package_path, original_backed_up , get_sys_prefix, get_py_version

from minimock import mock

base = os.getcwd()

mock('get_sys_prefix', returns='./testsrc/someuser/.virtualenvs/someenv/bin')
mock('get_py_version', returns='2.7')

def test_is_active_venv():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    assert active_venv() == True

def test_get_package_name():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    mock('os.path.expanduser', returns='./testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package')
    assert get_package_name() == 'some_package'

def test_get_active_venv():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    assert get_active_venv() == 'someenv'

def test_in_python_package():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    assert in_python_package() == True

# def test_in_python_package_nested_case():
#     mock('os.getcwd', returns='{}/tests/testsrc/someuser/src/some_package/some_package'.format(base))
#     assert in_python_package() == True

def test_get_envy_path():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    mock('os.path.expanduser', returns='./testsrc/someuser/.envies/someenv/some_package')
    assert get_envy_path() == './testsrc/someuser/.envies/someenv/some_package'

def test_get_package_name():
    mock('os.getcwd', returns= '{}/tests/testsrc/someuser/src/some_package'.format(base))
    mock('os.path.expanduser', returns='{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))
    print ('{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))
    assert get_venv_package_path() == '{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base)
