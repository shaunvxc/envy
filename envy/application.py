#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import argparse
import os
import re

from envy import VERSION

VENV_ROOT = "~/.virtualenvs/{}/lib/python{}/site-packages/{}"
ENVY_BASE = os.path.expanduser("~/.envies")

class helper(object):
    def get_sys_prefix(self):
        return sys.prefix

    def get_py_version(self):
        return str(sys.version_info.major) + "." + str(sys.version_info.minor)


helper = helper()

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
    return helper.get_sys_prefix()

def active_venv():
    return '/.virtualenvs/' in get_sys_prefix()

def get_active_venv():
    return re.search(".virtualenvs/([^/]{1,})/bin", get_sys_prefix()).group(1)

def in_python_package():
    return os.path.isfile(os.getcwd() + '/setup.py') or os.path.isfile(os.getcwd() + '/../setup.py')

def get_package_name():
    return os.getcwd().split("/")[-1]

def get_envy_path():
    return os.path.expanduser("~/.envies/{}/{}".format(get_active_venv(), get_package_name()))

def get_py_version():
    return helper.get_py_version()

def get_venv_package_path():
    package_name = get_package_name()
    venv = get_active_venv()

    if os.path.isdir(os.path.expanduser(VENV_ROOT.format(venv, get_py_version(), package_name))):
        return os.path.expanduser(VENV_ROOT.format(venv, get_py_version(), package_name))

    print("ERR: {}'s virtualenv does not contain {}".format(venv, package_name))
    print (os.path.expanduser(VENV_ROOT.format(venv, get_py_version(), package_name)))

    exit()

def original_backed_up():
    if not os.path.isdir(ENVY_BASE):
        os.system('mkdir {}'.format(ENVY_BASE))

    if not os.path.isdir(ENVY_BASE + "/{}".format(get_active_venv())):
        os.system('mkdir {}'.format(ENVY_BASE +  "/{}".format(get_active_venv())))

    return os.path.isdir(get_envy_path())

def back_up(venv_pkg_path):
    os.system("cp -r {} {}".format(venv_pkg_path, get_envy_path()))

def get_editor():
    config = ENVY_BASE + "/.editor.txt"
    editor = open(config).readline()
    return editor.rstrip()

@validate
def edit(args):
    base_path = "~/.virtualenvs/{}/lib/python{}/site-packages/".format(get_active_venv(), get_py_version())
    venv_pkg_path = get_venv_package_path()
    file_path = args.path[0]

    if not original_backed_up():
        print ("backing up {} ".format(venv_pkg_path))
        back_up(venv_pkg_path)

    if "/" not in args.path[0]:
        # file_path = args.path[0].split("/")[-1]
        base_path = venv_pkg_path

    editor = get_editor()
    os.system("{} {}/{} &".format(editor, base_path, file_path))

def set_editor(args):
    config = ENVY_BASE + "/.editor.txt"
    if not os.path.isfile(config):
        os.system('touch {}'.format(config))
        os.system('echo {} > {}'.format(args.editor[0], config))
    else:
        os.system('rm {}'.format(config))
        os.system('touch {}'.format(config))
        os.system('echo {} > {}'.format(args.editor[0], config))

@validate
def sync(args):
    venv_pkg_path = get_venv_package_path()

    if not original_backed_up():
        print ("backing up {} ".format(venv_pkg_path))
        back_up(venv_pkg_path)

    print ("Syncing local changes")

    if get_package_name() == args.path[0]:
        os.system("cp -r {} {}".format(args.path[0], venv_pkg_path + "/../"))
    else:
        os.system("cp -r {} {}".format(args.path[0], venv_pkg_path))

    print ("Local changes synced")

@validate
def clean(args):
    venv_pkg_path = get_venv_package_path()
    # remove applied changes
    print("cleaning local changes")
    os.system("rm -rf {}".format(venv_pkg_path))
    # copy over the original package from ~/.envies
    print ("restoring original virtualenv state")
    os.system("cp -r {} {}".format(get_envy_path(), venv_pkg_path))
    # remove envy backup
    print ("removing .envie")
    os.system("rm -rf {}".format(get_envy_path()))


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

    parser_editor = subparsers.add_parser('set-editor', help='edit dependency sourcefile')
    parser_editor.set_defaults(func=set_editor)
    parser_editor.add_argument('editor', nargs='*')

    return parser

def main():
    parser = prepare_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
