# -*- coding: utf-8 -*-

import os
import re
import pip

from .exceptions import NoVersionsError, PIPError, PkgNotFoundError
from .utils import ver_to_tuple
from .abc import ABCPackage

try:
    from urllib.request import urlopen
except Exception:
    from urllib import urlopen


class PyPIPackage(ABCPackage):
    __slots__ = ['pkg', 'has_custom_index', 'index', 'verbose']

    def __init__(self, pkg, index=None, verbose=False):
        """
        Args:
            pkg (str): name of package
            index (str): alternative index, if not given default for *pip* will be used. Include
                         full index url, e.g. https://example.com/simple
            verbose (bool): display verbose messages
        """
        self.pkg = pkg
        self.verbose = verbose
        if index:
            self.index = index.rstrip('/')
            self.has_custom_index = True
        else:
            self.index = "https://pypi.python.org/simple"
            self.has_custom_index = False

    def upgrade(self, dependencies=False, prerelease=False, force=False):
        """
        Upgrade the package unconditionaly
        Args:
            dependencies: update package dependencies if True (see pip --no-deps)
            prerelease: update to pre-release and development versions
            force: reinstall all packages even if they are already up-to-date
        Returns True if pip was sucessful
        """
        pip_args = ['install', self.pkg]

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

        if self.has_custom_index:
            pip_args.extend(['-i', self.index])

        try:
            ecode = pip.main(args=pip_args)
        except TypeError:
            # pip changed in 0.6.0 from initial_args to args, this is for
            # backwards compatibility can be removed when pip 0.5 is no longer
            # in use at all (approx. year 2025)
            ecode = pip.main(initial_args=pip_args)

        if ecode != 0:
            raise PIPError(ecode)

    def _get_newest_version(self):
        url = "{}/{}/".format(self.index, self.pkg)
        html = urlopen(url)
        if html.getcode() != 200:
            raise PkgNotFoundError
        pattr = re.compile(r'>{}-(.+?)<'.format(self.pkg), flags=re.I)
        versions = map(ver_to_tuple, pattr.findall(str(html.read())))
        if not versions:
            raise NoVersionsError
        return max(versions)
