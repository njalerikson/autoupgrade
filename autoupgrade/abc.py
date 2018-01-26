# -*- coding: utf-8 -*-

import sys
import os
from abc import (ABCMeta, abstractmethod)
import pkg_resources

from .utils import ver_to_tuple


class ABCPackage:
    # py2 backwards compatible
    __metaclass__ = ABCMeta

    # deprecated in favor of smartupgrade
    def upgrade_if_needed(self, *args, **kwargs):
        return self.smartupgrade(*args, **kwargs)

    def smartupgrade(self, restart=True, dependencies=False, prerelease=False):
        """
        Upgrade the package if there is a later version available.
        Args:
            restart: restart app if True
            dependencies: update package dependencies if True (see pip --no-deps)
            prerelease: update to pre-release and development versions
        """
        if not self.check():
            if self.verbose:
                print("Package {} already up-to-date!".format(self.pkg))
            return
        if self.verbose:
            print("Upgrading {} ... (v{} -> v{})".format(
                  self.pkg,
                  ".".join(map(str, self._get_current())),
                  ".".join(map(str, self._get_newest_version()))))
        self.upgrade(dependencies, prerelease, force=False)
        if restart:
            self.restart()

    @abstractmethod
    def upgrade(self, dependencies=False, prerelease=False, force=False):
        pass

    def restart(self):
        """
        Restart application with same args as it was started.
        Does **not** return
        """
        if self.verbose:
            print("Restarting {} {} ...".format(sys.executable, sys.argv))
        os.execl(sys.executable, *([sys.executable] + sys.argv))

    def check(self):
        """
        Check if pkg has a later version
        Returns true if later version exists
        """
        current = self._get_current()
        highest = self._get_newest_version()
        outdated = highest > current
        if self.verbose:
            if outdated:
                if current == (-1,):
                    print("{} is not installed!".format(self.pkg))
                else:
                    print("{} current version: {}".format(self.pkg, current))
                print("{} latest version:  {}".format(self.pkg, highest))
            else:
                print("{} is up-to-date!".format(self.pkg))
        return

    def _get_current(self):
        try:
            current = pkg_resources.get_distribution(self.pkg).version
            current = ver_to_tuple(current)
        except pkg_resources.DistributionNotFound:
            current = (-1,)
        return current

    @abstractmethod
    def _get_newest_version(self):
        pass

    def __str__(self):
        return self.pkg

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, str(self))
