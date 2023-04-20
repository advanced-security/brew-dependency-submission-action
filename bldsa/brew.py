import os
import json

from bldsa.dependencies import Dependency


def parseBrewEntry(name: str, data: dict) -> Dependency:
    """Parse a single Brew entry"""
    dep = Dependency(
        manager="brew",
        version=data.get("version"),
    )
    # remove version in name
    if "@" in name:
        name, _ = name.split("@", 1)

    # namespaces in name
    if "/" in name:
        # https://formulae.brew.sh/analytics/install/90d/
        bspace, btype, name = name.split("/", 2)

        if btype in ["tap", "taps", "cask"]:
            dep.namespace = bspace

    dep.name = name
    return dep


def parseBrewJson(data: dict) -> list[Dependency]:
    results = []
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


def parseBrewLock(path: str) -> list[Dependency]:
    """Parse Brewlock files

    https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#other-candidate-types-to-define
    """
    if not os.path.exists(path):
        raise Exception("Brew lock file does not exist")

    with open(path, "r") as handle:
        lock_data = json.load(handle)

    return parseBrewJson(lock_data)
