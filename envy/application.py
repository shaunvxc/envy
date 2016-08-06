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
from envy.decorators import validate_pkg, validate_env


def get_virtualenv():
    if 'VIRTUAL_ENV' in os.environ:
        return os.environ['VIRTUAL_ENV'].split('/')[-1]

    if 'WORKON_HOME' in os.environ:
        venv_root = os.environ['WORKON_HOME'].split('/')[-1]
        return re.search("{}/([^/]{{1,}})/bin".format(venv_root), sys.prefix).group(1)

    return re.search(".virtualenvs/([^/]{1,})/bin", sys.prefix).group(1)


def get_backup_base():
    return os.path.expanduser("~/.envies")


def get_backup_virtualenv():
    return get_backup_base() +  "/{}".format(get_virtualenv())


def get_package_name(target):
    if ('/' not in target and target.endswith('.py')) or target == '.':
        return os.getcwd().split("/")[-1]

    return target.split('/')[0]


def get_backup_package(target):
    return os.path.expanduser("~/.envies/{}/{}".format(get_virtualenv(), get_package_name(target)))


def get_package_path(target):
    return imp.find_module(get_package_name(target))[1]


def original_backed_up(target_package):
    if not os.path.isdir(get_backup_base()):
        os.makedirs('{}'.format(get_backup_base()))

    if not os.path.isdir(get_backup_virtualenv()):
        os.makedirs('{}'.format(get_backup_virtualenv()))

    return os.path.isdir(get_backup_package(target_package))


def back_up(package_path):
    shutil.copytree(package_path, get_backup_package(package_path.split('/')[-1]))


def get_editor():
    editor = os.environ.get('EDITOR', 'vi')
    if editor == 'vim': editor = 'vi' # vim does not like being launched from python
    return editor


def get_file_path(target):
    split_file_path = target.split("/")[1:]
    return "/".join(split_file_path)


@validate_env
def edit(args):
    package_path = get_package_path(args.path[0])
    if not original_backed_up(args.path[0]):
        print ("backing up {} ".format(package_path))
        back_up(package_path)
    else:
        print ("backup copy already exists...to restore it before applying new changes run `envy clean {}`".format(get_package_name(args.path[0])))

    file_path = get_file_path(args.path[0])
    editor = get_editor()
    subprocess.call([editor, os.path.join(package_path, file_path)], shell = (editor == 'vim'))


@validate_env
@validate_pkg
def sync(args):
    package_path = get_package_path(args.package[0])

    if not original_backed_up(args.package[0]):
        print ("backing up {} ".format(package_path))
        back_up(package_path)
    else:
        print ("backup copy already exists...to restore it before applying new changes run `envy clean {}`".format(args.package[0].split('/')[0]))

    try:
        print ("Syncing local changes")
        copytree(args.package[0], package_path)
        print ("Local changes synced")
    except Exception as e:
        clean(args)
        raise e


@validate_env
def clean(args):
    if args.all:
        for package in os.listdir(get_backup_virtualenv()):
            restore_environment(package)
    else:
        # needs to be args.package instead of args.package[0] here-- as we can also pass --all, making package technically
        # an optional argument, and hence we use nargs='?' instead of nargs=1.
        restore_environment(args.package)


@validate_env
def reset(args):
    if args.all:
        for package in os.listdir(get_backup_virtualenv()):
            reset_environment(package)
    else:
        # needs to be args.package instead of args.package[0] here-- as we can also pass --all, making package technically
        # an optional argument, and hence we use nargs='?' instead of nargs=1.
        reset_environment(args.package)


@validate_env
def diff(args):
    if not original_backed_up(args.path[0]):
        print ("no backup copy exists to diff with for  {}`".format(get_package_name(args.path[0])))
        return

    package_path = get_package_path(args.path[0])
    file_path = get_file_path(args.path[0])
    subprocess.call(['diff', os.path.join(package_path, file_path), os.path.join(get_backup_package(args.path[0]), file_path)])


def restore_environment(package_name):
    if not os.path.isdir(get_backup_package(package_name)):
        print ("uh oh..no recorded backup in {}".format(get_backup_package(package_name)))
        return

    package_path = get_package_path(package_name)
    print("cleaning applied changes for {}".format(package_name))
    shutil.rmtree(package_path)
    print ("restoring original {}'s virtualenv state".format(package_name))
    shutil.copytree(get_backup_package(package_name), package_path)

    if os.path.isdir(package_path):
        # ensure successful copy before removing the backup.
        print ("removing .envie")
        shutil.rmtree(get_backup_package(package_name))


def reset_environment(package_name):
    if not os.path.isdir(get_backup_package(package_name)):
        print ("uh oh..no recorded backup in {}, so nothing to reset".format(get_backup_package(package_name)))
        return

    print("dropping saved envie for {}".format(package_name))
    shutil.rmtree(get_backup_package(package_name))


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

    parser_edit = subparsers.add_parser('edit', help='edit dependency sourcefile')
    parser_edit.set_defaults(func=edit)
    parser_edit.add_argument('path', nargs=1)

    parser_clean = subparsers.add_parser('clean', help='reset virtualenv to original state')
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument('package', nargs='?',help='the name of the package to clean')
    parser_clean.add_argument('--all', action='store_true', help='clean all backed up environments')

    parser_sync = subparsers.add_parser('sync', help='sync all files to active virtualenv')
    parser_sync.set_defaults(func=sync)
    parser_sync.add_argument('package', nargs=1, help='the name of changes to sync-- can either be package_name or a path to a file including the package name (i.e. foo/bar.py , where foo is the package)')

    parser_diff = subparsers.add_parser('diff', help='get diff of current state of site-package against backed up copies')
    parser_diff.set_defaults(func=diff)
    parser_diff.add_argument('path', nargs=1)

    parser_reset = subparsers.add_parser('reset', help='reset the persisted backup copy of the provided package ')
    parser_reset.set_defaults(func=reset)
    parser_reset.add_argument('package', nargs='?')
    parser_reset.add_argument('--all', action='store_true', help='clean all backed up environments')

    return parser


def main():
    parser = prepare_parser()
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
