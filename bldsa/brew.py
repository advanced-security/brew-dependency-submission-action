import os
import json

from ghastoolkit.octokit.dependencygraph import Dependencies, Dependency


def parseBrewEntry(name: str, data: dict) -> Dependency:
    """Parse a single Brew entry"""
    dep_name = ""
    namespace = None
    # remove version in name
    if "@" in name:
        name, _ = name.split("@", 1)

    # namespaces in name
    if "/" in name:
        # https://formulae.brew.sh/analytics/install/90d/
        bspace, btype, dep_name = name.split("/", 2)

        if btype in ["tap", "taps", "cask"]:
            namespace = bspace
    else:
        dep_name = name

    return Dependency(
        dep_name,
        namespace=namespace,
        manager="brew",
        version=data.get("version"),
    )


def parseBrewJson(data: dict) -> Dependencies:
    results = Dependencies()

    brew_sys = data.get("system", {})
    brew_os = "macos" if brew_sys.get("macos") else "deb"

    for dep_name, dep_data in data.get("entries", {}).get("brew", {}).items():
        results.append(parseBrewEntry(dep_name, dep_data))

    for dep_name, dep_data in data.get("entries", {}).get("cask", {}).items():
        results.append(
            Dependency(
                manager="brew",
                name=dep_name,
                version=dep_data.get("version"),
            )
        )

    return results


def parseBrewLock(path: str) -> Dependencies:
    """Parse Brewlock files

    https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#other-candidate-types-to-define
    """
    if not os.path.exists(path):
        raise Exception("Brew lock file does not exist")

    with open(path, "r") as handle:
        lock_data = json.load(handle)

    return parseBrewJson(lock_data)
