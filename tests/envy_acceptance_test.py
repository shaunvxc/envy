import sys
import os
import envy
import pkg_resources

from envy import get_active_venv, get_package_name, get_envy_path, original_backed_up, get_venv_full_package_path, sync, clean
from envy.decorators import is_active_venv, in_python_package

from mock import MagicMock, PropertyMock
from mock import patch
import argparse

## TODO: Add test for deeply nested files

base = os.getcwd()

def setup_test(f):
    """
    All of this patching is annoying, but seems to be the best way to do acceptance testing on envy.
    In the test folder, we have keep a file structure consistent with a common structured of a file system
    with virtual envs.  However, because all of this structure is contained within the test folder of this
    project-- thereby *NOT* real virtual environments-- all of the code responsible for doing this sort of
    thing IRL won't work on this dummy data.  So, we patch it all and let the code responsible for backing
    up copies and moving changes around work with mocked paths.

    The idea is that the acceptance tests + the tests in envy_test.py will (hopefully) provide enough coverage.
    """
    def wrap_patches(*args, **kwargs):
        with patch('envy.decorators.is_active_venv', return_value=True):
            with patch('envy.application.get_active_venv', return_value="someenv"):
                with patch('envy.decorators.in_python_package', return_value=True):
                    with patch('envy.application.get_envy_base', return_value="{}/tests/testsrc/someuser/.envies/".format(base)):
                        with patch('envy.application.get_envy_path', return_value="{}/tests/testsrc/someuser/.envies/someenv/some_package".format(base)):
                            with patch('envy.application.get_venv_full_package_path', return_value='{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base)):
                                with patch('os.path.expanduser', return_value="{}/tests/testsrc/someuser/src/some_package/some_package".format(base)):
                                    return f(*args, **kwargs)

    return wrap_patches

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@setup_test
def test_sync_package_and_clean(mock_os):

    args = argparse.Namespace()
    args.package = ['some_package/test.py']

    sync(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == True
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == True

    args.all = False

    clean(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == False
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == False

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@setup_test
def test_sync_file_and_clean(mock_os):

    args = argparse.Namespace()
    args.package = ['some_package/test.py']

    sync(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == True
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == True

    args.all = True
    clean(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == False
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == False


@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package/some_package'.format(base))
@setup_test
def test_sync_file_from_inner_dir_and_clean(mock_os):

    args = argparse.Namespace()
    args.package = ['test.py']

    sync(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == True
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == True

    args.all = False
    clean(args)


    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == False
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == False
