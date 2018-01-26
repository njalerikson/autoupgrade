# -*- coding: utf-8 -*-

from unittest import TestCase

from autoupgrade import Package
from autoupgrade.utils import ver_to_tuple


class TestFunctions(TestCase):

    def test_ver_to_tuple(self):
        self.assertGreater(
            ver_to_tuple('0.1.2'),
            ver_to_tuple('0.1.1'))
        self.assertGreater(
            ver_to_tuple('0.1.5A'),
            ver_to_tuple('0.1.5'))
        self.assertGreater(
            ver_to_tuple('0.10.0'),
            ver_to_tuple('0.9.5'))
        self.assertGreater(
            ver_to_tuple('1.2.3'),
            ver_to_tuple('1.2'))
        self.assertGreater(
            ver_to_tuple('1.2A.3'),
            ver_to_tuple('1.2.3'))
        self.assertEqual(
            ver_to_tuple('1.2.3'),
            ver_to_tuple('1.2.3'))

    def test_pypi_upgrade_default(self):
        inst = Package.pypi(
            pkg="pip",
            verbose=True)
        inst.smartupgrade(restart=False)

    def test_pypi_upgrade_index(self):
        inst = Package.pypi(
            pkg="pip",
            index="https://pypi.python.org/simple",
            verbose=True)
        inst.smartupgrade(restart=False)

    def test_github_upgrade_default(self):
        inst = Package.github(
            pkg="autoupgrade",
            user="vuolter",
            repo="autoupgrade-ng",
            verbose=True)
        inst.smartupgrade(restart=False)
