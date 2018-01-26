# AutoUpgrade
[![PyPI](https://img.shields.io/pypi/v/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![GitHub issues](https://img.shields.io/github/issues/vuolter/autoupgrade.svg)](https://github.com/vuolter/autoupgrade/issues)
[![PyPI](https://img.shields.io/pypi/dm/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![PyPI](https://img.shields.io/pypi/l/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![PyPI](https://img.shields.io/pypi/format/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![PyPI](https://img.shields.io/pypi/pyversions/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![PyPI](https://img.shields.io/pypi/status/autoupgrade-ng.svg)](https://pypi.python.org/pypi/autoupgrade-ng)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/WalterPurcaro.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

Automatic upgrade of PyPI packages or GitHub repos.


## Table of contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Licensing](#licensing)


## Quick Start

    from autoupgrade import Package
    Package(<packagename>).smartupgrade()

Example:

    from autoupgrade import Package
    Package('pip').smartupgrade()

The above will upgrade the Python package `pip` only if there is a new version
available on the PyPI.
The upgrade will be unattended and the python script will be restarted.

Old methods are still supported; you can accomplish the same task calling:

    from autoupgrade import AutoUpgrade
    AutoUpgrade('pip').upgrade_if_needed()


## Installation

    pip install autoupgrade-ng

All the modules will be installed under the _autoupgrade_ package, so **make
sure you have already removed the old [AutoUpgrade package]
(https://pypi.python.org/pypi/autoupgrade) before install this** to avoid an
installation conflict.


## API

### Classes

#### class autoupgrade.abc.ABCPackage(object)

Abstract class that defines the structure of an `autoupgrade` package.

#### class autoupgrade.pypi.PyPIPackage(autoupgrade.abc.ABCPackage)

Basic package class for PyPI, holds one package.

    __init__(self, pkg, index=None, verbose=False)

**Arguments**:

- `pkg` (str) name of package.
- `index` (str) alternative index, if not given default from *pip* will be used.
Include full index url *(e.g. https://example.com/simple)*.
- `verbose` (bool) print verbose statements.

**Return**: None.

#### class autoupgrade.github.GitHubPackage(autoupgrade.abc.ABCPackage)

Basic package class for GitHub, holds one repository.

    __init__(self, pkg, user, repo=None, authenticate=(), verbose=False)

**Arguments**:

- `pkg` (str) name of package.
- `user` (str) name of the GitHub user/organization that the repo belongs to.
- `repo` (None, str) if the repo doesn't match the `pkg` name.
- `authenticate` (tuple) login credentials to login to GitHub (see
[github package](https://github.com/PyGithub/PyGithub)) this likely will just be
`(<username>, <password>)` or `(<API token>)`
- `verbose` (bool) print verbose statements.

**Return**: None.

#### class autoupgrade.package.Package(object)

Basic class used to bundle PyPIPackage and GitHubPackage.

    __init__(self, *args, **kwargs)

**Arguments**: provide arguments for `PyPIPackage` **or** `GitHubPackage` and the
applicable package will be created. Alternatively access the class method
corresponding to the package type you wish to initialize
(e.g. `Package.pypi(*args, **kwargs)` versus `Package.github(*args, **kwargs)`.

**Return**: None.

#### class autoupgrde.AutoUpgrade(autoupgrade.package.Package)

**(Deprecated, see Package)**


### Methods for PyPIPackage & GitHubPackage

    smartupgrade(self, restart=True, dependencies=False, prerelease=False)

Upgrade the package if there is a newer version available.

**Arguments**:

- `restart` restart app if True.
- `dependencies` update dependencies if True *(see `pip --no-deps`)*.
- `prerelease` update to pre-release and development versions.

**Return**: None.

    upgrade_if_needed(self, restart=True, dependencies=False, prerelease=False)

**(Deprecated, see smartupgrade)**

    upgrade(self, dependencies=False, prerelease=False, force=False)

Upgrade the package unconditionally.

**Arguments**:

- `dependencies` update dependencies if True *(see `pip --no-deps`)*.
- `prerelease` update to pre-release and development versions.
- `force` reinstall all packages even if they are already up-to-date.

    check(self)

Check if `pkg` has a newer version.

**Arguments**: None.

**Return**: True if a newer version exists, else False.

    restart(self)

Restart application with same args as it was started.

**Arguments**: None.

**Return**: None.


## Licensing

Please refer to the included [LICENSE](/LICENSE.md) for the extended license.


----------------------------
###### © 2017 Walter Purcaro
