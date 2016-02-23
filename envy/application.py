#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import argparse
import os
import re
import pkg_resources
import shutil
import subprocess

from envy import VERSION
ENVY_BASE = os.path.expanduser("~/.envies")

def validate(f):
    def wrapper(args):
        if not active_venv():
            print("ERR: No active virtual env!")
            return False

        if not in_python_package():
            print("ERR: must be run from within a python package")
            return False

        return f(args)
    return wrapper

def get_sys_prefix():
    return sys.prefix

def active_venv():
    """
    Return True if we're running inside a virtualenv, False otherwise.
    """
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True

    return False

def get_active_venv():
    return re.search(".virtualenvs/([^/]{1,})/bin", get_sys_prefix()).group(1)

def in_python_package():
    return os.path.isfile(os.getcwd() + '/setup.py') or os.path.isfile(os.getcwd() + '/../setup.py')

def get_package_name():
    return os.getcwd().split("/")[-1]

def get_envy_path():
    return os.path.expanduser("~/.envies/{}/{}".format(get_active_venv(), get_package_name()))

def get_venv_base_package_path():
    return pkg_resources.get_distribution(get_package_name()).location

def get_venv_full_package_path():
    return get_venv_base_package_path() + "/{}".format(get_package_name())

def original_backed_up():
    if not os.path.isdir(ENVY_BASE):
        os.makedirs('{}'.format(ENVY_BASE))

    if not os.path.isdir(ENVY_BASE + "/{}".format(get_active_venv())):
        os.makedirs('{}'.format(ENVY_BASE +  "/{}".format(get_active_venv())))

    return os.path.isdir(get_envy_path())

def back_up(venv_pkg_path):
    shutil.copytree(venv_pkg_path, get_envy_path())

def get_editor():
    if 'EDITOR' in os.environ:
        return os.environ['EDITOR']

    print ("No $EDITOR system env var specified specified, defaulting to vim...")
    return 'vim'

@validate
def edit(args):
    edit_path = get_venv_base_package_path()
    full_package_path = get_venv_full_package_path()

    file_path = args.path[0]

    if not original_backed_up():
        print ("backing up {} ".format(full_package_path))
        back_up(full_package_path)

    if "/" not in args.path[0]:
        edit_path = full_package_path

    editor = get_editor()
    subprocess.call([editor, os.path.join(edit_path, file_path)], shell = (editor == 'vim'))

@validate
def sync(args):
    venv_pkg_path = get_venv_full_package_path()

    if not original_backed_up():
        print ("backing up {} ".format(venv_pkg_path))
        back_up(venv_pkg_path)

    try:
        print ("Syncing local changes")
        copytree(args.path[0], venv_pkg_path)
        print ("Local changes synced")
    except Exception as e:
        clean(args)
        raise e

@validate
def clean(args):
    if not os.path.isdir(get_envy_path()):
        print ("uh oh..no recorded backup in {}".format(get_envy_path()))
        return

    venv_pkg_path = get_venv_full_package_path()
    # remove applied changes
    print("cleaning local changes")

    shutil.rmtree(venv_pkg_path)
    print ("restoring original virtualenv state")
    shutil.copytree(get_envy_path(), venv_pkg_path)

    if os.path.isdir(venv_pkg_path):
        # ensure successful copy before removing the backup.
        print ("removing .envie")
        shutil.rmtree(get_envy_path())

def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)

    if os.path.isfile(src):
        shutil.copy2(src, dst)
        return

    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)

    subparsers = parser.add_subparsers(dest='command_name')

    parser_sync = subparsers.add_parser('sync', help='sync all files to active virtualenv')

    parser_sync.set_defaults(func=sync)
    parser_sync.add_argument('path', nargs='*')

    parser_clean = subparsers.add_parser('clean', help='reset virtualenv to original state')
    parser_clean.set_defaults(func=clean)

    parser_edit = subparsers.add_parser('edit', help='edit dependency sourcefile')
    parser_edit.set_defaults(func=edit)
    parser_edit.add_argument('path', nargs='*')

    return parser

def main():
    parser = prepare_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
