# -*- coding: utf-8 -*-

from .github import GitHubPackage
from .pypi import PyPIPackage


class Package(object):
    __preferred = [PyPIPackage, GitHubPackage]

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

    @classmethod
    def github(cls, *args, **kwargs):
        return GitHubPackage(*args, **kwargs)
