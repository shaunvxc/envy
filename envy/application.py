#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import argparse
import os
import re
import imp
import shutil
import subprocess

from envy import VERSION

def get_envy_base():
    return os.path.expanduser("~/.envies")

def validate_env(f):
    def wrapper(args):
        if not active_venv():
            print("ERR: No active virtual env!")
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

def active_venv():
    """
    Return True if we're running inside a virtualenv, False otherwise.
    """
    if hasattr(sys, 'real_prefix'):
        return True

    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True

    return False

def get_active_venv():
    return re.search(".virtualenvs/([^/]{1,})/bin", sys.prefix).group(1)

def in_python_package():
    return os.path.isfile(os.getcwd() + '/setup.py') or os.path.isfile(os.getcwd() + '/../setup.py')

def get_package_name():
    return os.getcwd().split("/")[-1]

def get_envy_path(pkg_name=None):
    if pkg_name is None:
        return os.path.expanduser("~/.envies/{}/{}".format(get_active_venv(), get_package_name()))
    return os.path.expanduser("~/.envies/{}/{}".format(get_active_venv(), pkg_name))

def get_venv_full_package_path(pkg_name=None):
    if pkg_name is None:
        return imp.find_module(get_package_name())[1]

    return imp.find_module(pkg_name)[1]

def original_backed_up():
    if not os.path.isdir(get_envy_base()):
        os.makedirs('{}'.format(get_envy_base()))

    if not os.path.isdir(get_envy_base() + "/{}".format(get_active_venv())):
        os.makedirs('{}'.format(get_envy_base() +  "/{}".format(get_active_venv())))

    return os.path.isdir(get_envy_path())

def back_up(venv_pkg_path, pkg_name=None):
    shutil.copytree(venv_pkg_path, get_envy_path(pkg_name))

def get_editor():
    if 'EDITOR' in os.environ:
        return os.environ['EDITOR']

    print ("No $EDITOR system env var specified specified, defaulting to vim...")
    return 'vim'

@validate_env
def edit(args):
    pkg_name_given_in_arg = None

    if '/' in args.path[0]:
        pkg_name_given_in_arg = args.path[0].split('/')[0]

    full_package_path = get_venv_full_package_path(pkg_name_given_in_arg)

    file_path = args.path[0].split("/")[-1]

    if not original_backed_up():
        print ("backing up {} ".format(full_package_path))
        back_up(full_package_path, pkg_name_given_in_arg)

    editor = get_editor()
    subprocess.call([editor, os.path.join(full_package_path, file_path)], shell = (editor == 'vim'))

@validate_env
@validate_pkg
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

@validate_env
def clean(args):
    if not os.path.isdir(get_envy_path(args.path)):
        print ("uh oh..no recorded backup in {}".format(get_envy_path(args.path)))
        return

    venv_pkg_path = get_venv_full_package_path(args.path)
    print("cleaning applied changes")
    shutil.rmtree(venv_pkg_path)
    print ("restoring original virtualenv state")
    shutil.copytree(get_envy_path(args.path), venv_pkg_path)

    if os.path.isdir(venv_pkg_path):
        # ensure successful copy before removing the backup.
        print ("removing .envie")
        shutil.rmtree(get_envy_path(args.path))

def copytree(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)

    if os.path.isfile(src):
        shutil.copy2(src, dst)
        return

    if not os.path.isdir(src):
        src = os.path.expanduser(src)

    for item in os.listdir(src):
        ss = os.path.join(src, item)
        dd = os.path.join(dst, item)
        if os.path.isdir(ss):
            copytree(ss, dd)
        else:
            shutil.copy2(ss, dd)

def prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)

    subparsers = parser.add_subparsers(dest='command_name')

    parser_sync = subparsers.add_parser('sync', help='sync all files to active virtualenv')

    parser_sync.set_defaults(func=sync)
    parser_sync.add_argument('path', nargs='*')

    parser_clean = subparsers.add_parser('clean', help='reset virtualenv to original state')
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument('-p', '--path')

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
