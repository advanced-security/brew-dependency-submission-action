import unittest

from bldsa.brew import parseBrewEntry


class EntryTest(unittest.TestCase):
    def test_parseBrewEntryNames(self):
        data = {
            "version": "3.10.10_1",
        }
        dep = parseBrewEntry("python@3.10", data)
        self.assertEqual(dep.name, "python")
        self.assertEqual(dep.version, "3.10.10_1")

        data = {
            "version": "11.0.18",
        }
        dep = parseBrewEntry("openjdk@11", data)
        self.assertEqual(dep.name, "openjdk")
        self.assertEqual(dep.version, "11.0.18")

    def test_parseBrewEntryGitHub(self):
        # github/bootstrap/elasticsearch@2.4
        data = {
            "version": "2.4.6_1",
        }
        dep = parseBrewEntry("github/bootstrap/elasticsearch@2.4", data)
        self.assertEqual(dep.name, "elasticsearch")
        self.assertEqual(dep.version, "2.4.6_1")

        # github/bootstrap/elasticsearch@2.4
        data = {
            "version": "2020-9-29-1+git@f6394cf",
        }
        dep = parseBrewEntry("github/packages/awssume", data)
        self.assertEqual(dep.name, "awssume")
        self.assertEqual(dep.version, "2020-9-29-1+git@f6394cf")

    def test_parseBrewEntryTap(self):
        # https://formulae.brew.sh/analytics/install/90d/
        # TODO is this correct or should it be kyoh86/richgo?
        data = {
            "version": "0.3.12",
        }
        dep = parseBrewEntry("kyoh86/tap/richgo", data)

        self.assertEqual(dep.namespace, "kyoh86")
        self.assertEqual(dep.name, "richgo")
        self.assertEqual(dep.version, "0.3.12")
