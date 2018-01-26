# -*- coding: utf-8 -*-

from .exceptions import PIPError

from .pypi import PyPIPackage
try:
    from .github import GitHubPackage
except ImportError:
    GitHubPackage = None


class Package(object):
    __preferred = [PyPIPackage]

    def __new__(cls, *args, **kwargs):
        # to keep track of the first error (if there was one)
        first_error = None

        # loop over the preferred order of the package handlers, for each one
        # try to initialize, if it fails to initialize then continue to the
        # next preferred package handler
        for pkg_type in cls.__preferred:
            try:
                # return a successful package handler match
                return pkg_type(*args, **kwargs)
            except TypeError as e:
                # only remember the very first error thrown as that is the most
                # preferred package handler
                if first_error is None:
                    first_error = e

        # raise an error if there was no preferred handler match
        if first_error is None:
            err = ("This {} has no preferred package handlers "
                   "(__preferred == {})").format(
                   cls.__name__,
                   cls.__preferred)
            raise TypeError(err)
        raise first_error

    @classmethod
    def pypi(cls, *args, **kwargs):
        return PyPIPackage(*args, **kwargs)


# only add the GitHubPackage if it was imported properly
if GitHubPackage is not None:
    class Package(Package):
        __preferred = [PyPIPackage, GitHubPackage]

        @classmethod
        def github(cls, *args, **kwargs):
            return GitHubPackage(*args, **kwargs)


# deprecated in favor of Package
class AutoUpgrade(Package):
    def upgrade(self, *args, **kwargs):
        try:
            Package.upgrade(self, *args, **kwargs)
        except PIPError:
            return False
        else:
            return True
