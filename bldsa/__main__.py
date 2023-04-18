import os
import json
import argparse

from bldsa.dependencies import Dependency, exportDependencies 
from bldsa.octokit import Octokit


parser = argparse.ArgumentParser(__name__)

parser.add_argument("-i", "--brewlock", help="Brewlock file location")

parser.add_argument("-sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("-ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-gr",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "-gi",
    "--github-instance",
    help="GitHub Instance",
)
parser_github.add_argument(
    "-t",
    "-gt",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)


def findBrewFiles(path: str) -> list[str]:
    """ Find all the Brewfiles """
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file == "Brewfile.lock.json":
                results.append(os.path.join(root, file))
    return results


def parseBrewLock(path: str) -> list[Dependency]:
    """ Parse Brewlock files 

    https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#other-candidate-types-to-define
    """
    if not os.path.exists(path):
        raise Exception("Brew lock file does not exist")

    results = []
    with open(path, "r") as handle:
        lock_data = json.load(handle)

    brew_sys = lock_data.get("system", {})
    brew_os = "macos" if brew_sys.get("macos") else "deb"

    for dep_name, dep_data in lock_data.get("entries", {}).get("brew", {}).items():
        # TODO redo these parts
        # What about taps?
        if "@" in dep_name:
            dep_name, _ = dep_name.split("@", 1)
        dep_name = dep_name.replace("github/bootstrap/", "")
        dep_name = dep_name.replace("github/packages/", "")
        
        results.append(
            Dependency(
                manager="brew",
                name=dep_name,
                version=dep_data.get("version"),
            )
        )

    for dep_name, dep_data in lock_data.get("entries", {}).get("cask", {}).items():
        results.append(
            Dependency(
                manager="brew",
                name=dep_name,
                version=dep_data.get("version"),
            )
        )
    return results



if __name__ == "__main__":
    arguments = parser.parse_args()

    lock_files = []

    owner, repo = arguments.github_repository.split("/", 1)
    octokit = Octokit(owner, repo, arguments.github_token)

    if arguments.brewlock:
        lock_files.append(arguments.brewlock)
    else:
        lock_files = findBrewFiles(".")
   
    for lockfile in lock_files:
        print(f"Lockfile found :: {lockfile}")
        
        dependencies = parseBrewLock(lockfile)

        bom = exportDependencies(
            lockfile,
            dependencies,
            sha=arguments.sha,
            ref=arguments.ref
        ) 
        print(json.dumps(bom, indent=2))

        octokit.submitDependencies(bom)

