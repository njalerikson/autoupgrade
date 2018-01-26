# -*- coding: utf-8 -*-

import github
import pip
import os

from .exceptions import PIPError
from .abc import ABCPackage
from .utils import ver_to_tuple


class GitHubPackage(ABCPackage):
    __slots__ = ['pkg', 'repository', 'verbose']

    def __init__(self, pkg, user, repo=None, authenticate=(), verbose=False):
        """
        Args:
            repo (str): GitHub repo
            user (str): GitHub user/organization
            verbose (bool): display verbose messages
        """
        if repo is None:
            repo = pkg

        self.pkg = pkg
        gh = github.Github(*authenticate)
        usr = gh.get_user(user)
        self.repository = usr.get_repo(repo)
        self.verbose = verbose

    def upgrade(self, dependencies=False, prerelease=False, force=False):
        """
        Upgrade the package unconditionaly
        Args:
            dependencies: update package dependencies if True (see pip --no-deps)
            prerelease: update to pre-release and development versions
            force: reinstall all packages even if they are already up-to-date
        Returns True if pip was sucessful
        """
        pip_args = ['install']

        found = self._get_current() != (-1)
        if found:
            pip_args.append("--upgrade")

        if force:
            pip_args.append("--force-reinstall")

        if not dependencies:
            pip_args.append("--no-deps")

        if prerelease:
            pip_args.append("--pre")

        proxy = os.environ.get('http_proxy')
        if proxy:
            pip_args.extend(['--proxy', proxy])

        pip_args.append(self._get_latest_release().raw_data["zipball_url"])

        try:
            ecode = pip.main(args=pip_args)
        except TypeError:
            # pip changed in 0.6.0 from initial_args to args, this is for
            # backwards compatibility can be removed when pip 0.5 is no longer
            # in use at all (approx. year 2025)
            ecode = pip.main(initial_args=pip_args)

        if ecode != 0:
            raise PIPError(ecode)

    def _get_latest_release(self):
        return next(iter(self.repository.get_releases()))

    def _get_newest_version(self):
        return ver_to_tuple(self._get_latest_release().tag_name)
