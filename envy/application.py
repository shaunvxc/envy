#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import argparse
import os
import re

from envy import VERSION, SUPPORTED_PYTHON_VERSIONS

VENV_ROOT = "~/.virtualenvs/{}/lib/python{}/site-packages/{}"
ENVY_BASE = os.path.expanduser("~/.envies")

def validate(f):
    def wrapper(*args):
        if not active_venv():
            print("ERR: No active virtual env!")
            return False

        if not in_python_package():
            print("ERR: must be run from within a python package")
            return False

        return f(args)

    return wrapper

def active_venv():
    return '/.virtualenvs/' in sys.prefix

def get_active_venv():
    return re.search(".virtualenvs/([^/]{1,})/bin", sys.prefix).group(1)

def in_python_package():
    path = os.getcwd()

    return os.path.isfile(path + '/setup.py') or os.path.isfile(path + '/../setup.py')

def get_package_name():
    return os.getcwd().split("/")[-1]

def get_envy_path():
    return os.path.expanduser("~/.envies/{}/{}".format(get_active_venv(), get_package_name()))

# def get_py_version(venv):
#     return re.search("/.virtualenvs/{}/lib/python([2-3].[2-7])".format(venv), venv).group

def get_venv_package_path():
    package_name = get_package_name()
    venv = get_active_venv()

    for py_version in SUPPORTED_PYTHON_VERSIONS:
        if os.path.isdir(os.path.expanduser(VENV_ROOT.format(venv, py_version, package_name))):
            return os.path.expanduser(VENV_ROOT.format(venv, py_version, package_name))


    print("ERR: {}'s virtualenv does not contain {}".format(venv_name, project_name))
    exit()


def original_backed_up():
    if not os.path.isdir(ENVY_BASE):
        os.system('mkdir {}'.format(ENVY_BASE))

    if not os.path.isdir(ENVY_BASE + "/{}".format(get_active_venv())):
        os.system('mkdir {}'.format(ENVY_BASE +  "/{}".format(get_active_venv())))

    return os.path.isdir(get_envy_path())

def back_up(venv_pkg_path):
    os.system("cp -r {} {}".format(venv_pkg_path, get_envy_path()))

@validate
def sink_all(*args):
    venv_pkg_path = get_venv_package_path()

    if not original_backed_up():
        back_up(venv_pkg_path)

    # os.system("python setup.py install")
    os.system("cp *.py {}".format(venv_pkg_path))

    print ("Sinked")

@validate
def sink_clean(*args):
    venv_pkg_path = get_venv_package_path()
    # remove applied changes
    os.system("rm -rf {}".format(venv_pkg_path))
    # copy over the original package from ~/.envies
    os.system("cp -r {} {}".format(get_envy_path(), venv_pkg_path))
    # remove envy backup
    os.system("rm -rf {}".format(get_envy_path()))


def prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)

    subparsers = parser.add_subparsers(dest='command_name')

    parser_search = subparsers.add_parser('all', help='sync all files to active virtualenv')

    parser_search.set_defaults(func=sink_all)
    parser_search.add_argument('filename', nargs='*')

    parser_list = subparsers.add_parser('clean', help='reset virtualenv to original state')
    parser_list.set_defaults(func=sink_clean)

    return parser


def main():
    parser = prepare_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
