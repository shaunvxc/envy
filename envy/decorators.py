import os
import sys

def validate_env(f):
    def wrapper(args):
        if not is_active_venv():
            print("ERR: `envy` must be run from within an active virtualenv!")
            return False
        return f(args)
    return wrapper


def validate_pkg(f):
    def wrapper(args):
        if not in_python_package():
            print("ERR: must be run from within a python package")
            return False
        return f(args)
    return wrapper


def is_active_venv():
    if hasattr(sys, 'real_prefix'):
        return True

    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True

    return False


def in_python_package():
    return os.path.isfile(os.getcwd() + '/setup.py') or os.path.isfile(os.getcwd() + '/../setup.py')
