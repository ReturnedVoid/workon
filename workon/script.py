"""Script main module."""
import glob
import logging
import os
import shutil
import subprocess

from . import git
from .errors import ScriptError


def _remove_project(project, directory, force):
    logging.info('Finishing up "%s"', project)
    proj_path = os.path.join(directory, project)

    if not git.is_stash_empty(proj_path) and not force:
        raise ScriptError(
            'Wait a moment, you have left some stashes! If you are confident, '
            'use "-f" flag'
        )

    unpushed_info = git.get_unpushed_branches_info(proj_path)
    if unpushed_info and not force:
        raise ScriptError(
            'Wait a moment, you left some unpushed commits! Please, '
            'take a look:\n%s\n\nIf you are confident, use "-f" flag'
            % unpushed_info
        )

    unstaged_changes = git.get_unstaged_info(proj_path)
    if unstaged_changes and not force:
        raise ScriptError(
            'Wait a moment, you left some unstaged changes! Please, '
            'take a look:\n%s\n\nIf you are confident, use "-f" flag'
            % unstaged_changes
        )

    logging.debug('Removing "%s"', proj_path)
    shutil.rmtree(proj_path)


def done(args):
    """Finish up with a project(s)."""
    try:
        projects = os.listdir(args.directory)
    except OSError as exc:
        raise ScriptError(
            'Oops, can\'t access working directory: %s' % exc) from exc

    if args.project:
        if args.project not in projects:
            raise ScriptError(
                '"%s" not found in "%s"' % (args.project, args.directory))
        _remove_project(args.project, args.directory, args.force)
    else:
        for project in projects:
            if os.path.isdir(os.path.join(args.directory, project)):
                try:
                    _remove_project(project, args.directory, args.force)
                except ScriptError as exc:
                    logging.error(exc)
                    continue
        # there may be some files left
        for filepath in glob.glob(os.path.join(args.directory, '*')):
            if os.path.isfile(filepath):
                os.remove(filepath)


def start(args):
    """Start your work on a project.

    * clones the project from GIT
    * checks if working directory is empty
    """
    logging.info('Setting up "%s"', args.project)

    project_path = args.source.strip('/') + '/' + args.project + '.git'
    destination = args.directory + '/{}'.format(args.project)
    git.clone(project_path, destination)

    if not args.noopen:
        _open_project(args)


def open(args):
    """Open the project in specified editor."""
    _open_project(args)


def _open_project(args):
    logging.info('Opening "%s"', args.project)
    project_dir = os.path.join(args.directory, args.project)

    if not os.path.isdir(project_dir):
        raise ScriptError(
            'No project named "%s" found under your working directory'
            % args.project
        )

    for editor in (args.editor, os.environ.get('EDITOR'), 'vi', 'vim'):
        if editor:
            logging.info('Trying to open project with "%s"', editor)
            try:
                result = subprocess.run([editor, project_dir], check=False)
            except OSError as exc:
                logging.error(
                    'Failed to open "%s" with "%s": %s',
                    args.project, args.editor, exc
                )
            else:
                if result.returncode == 0:
                    break
    else:
        raise ScriptError('No suitable editor found to open your project')
