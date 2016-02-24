import sys
import os
import envy
import pkg_resources

from envy import active_venv, get_active_venv, in_python_package, get_package_name, get_envy_path,  original_backed_up, get_venv_full_package_path, sync, clean

from mock import MagicMock, PropertyMock
from mock import patch
import argparse

base = os.getcwd()

# def setup_test(f):
#     @patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
#     def wrap_patches(*args, **kwargs):
#         with patch('envy.application.sys.prefix', "./testsrc/someuser/.virtualenvs/someenv/bin"):
#             with patch('envy.application.imp.find_module', return_value=(None,'{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))):
#                 return f(*args, **kwargs)

#     return wrap_patches

@patch('os.getcwd', return_value='{}/tests/testsrc/someuser/src/some_package'.format(base))
@patch('envy.application.active_venv', return_value=True)
@patch('envy.application.in_python_package', return_value=True)
@patch('envy.application.get_envy_base', return_value="{}/tests/testsrc/someuser/.envies/")
@patch('envy.application.get_envy_path', return_value="{}/tests/testsrc/someuser/.envies/someenv/some_package".format(base))
@patch('envy.application.get_venv_full_package_path', return_value='{}/tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package'.format(base))
@patch('os.path.expanduser', return_value="{}/tests/testsrc/someuser/src/some_package/some_package".format(base))
def test_sync_and_clean(dummy1, dummy2, dummy3,dummy4, dummy5, dummy6,  mock_os):

    args = argparse.Namespace()
    args.path = ['some_package']

    sync(args)

    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == True
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == True

    clean(args)
    
    assert os.path.isdir('./tests/testsrc/someuser/.envies/someenv/some_package') == False
    assert os.path.isfile('./tests/testsrc/someuser/.virtualenvs/someenv/lib/python2.7/site-packages/some_package/test.py') == False

    
