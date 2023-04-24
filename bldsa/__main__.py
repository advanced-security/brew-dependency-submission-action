import json
import os
import logging
import argparse

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.dependencygraph import DependencyGraph

from bldsa import __name__ as tool_name
from bldsa.brew import parseBrewLock


logger = logging.getLogger(tool_name)
parser = argparse.ArgumentParser(tool_name)

parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
parser.add_argument("-i", "--brewlock", help="Brewlock file location")

parser.add_argument("-sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("-ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-r",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "--github-instance",
    default=os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
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
    """Find all the Brewfiles"""
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file == "Brewfile.lock.json":
                results.append(os.path.join(root, file))
    return results


if __name__ == "__main__":
    arguments = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG
        if arguments.debug or os.environ.get("DEBUG")
        else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    lock_files = []

    GitHub.init(
        repository=arguments.github_repository,
        token=arguments.github_token,
        instance=arguments.github_instance,
    )
    if not GitHub.repository:
        raise Exception("Repository not set")

    depgraph = DependencyGraph(GitHub.repository)
    logger.debug(f"GitHub Instance :: {GitHub}")

    if arguments.brewlock:
        lock_files.append(arguments.brewlock)
    else:
        lock_files = findBrewFiles(".")

    for lockfile in lock_files:
        logger.info(f"Lockfile found :: {lockfile}")

        dependencies = parseBrewLock(lockfile)

        logger.debug(f"Dependencies Count :: {len(dependencies)}")

        if not arguments.dry_run:
            depgraph.submitDependencies(
                dependencies, tool_name, lockfile, sha=arguments.sha, ref=arguments.ref
            )

            logger.info("Submitted BOM!")
        else:
            logger.info("Dry run mode, skipping submission")
            print(
                json.dumps(
                    dependencies.exportBOM(
                        tool_name, lockfile, sha=arguments.sha, ref=arguments.ref
                    ),
                    indent=2,
                )
            )

    logger.info("Done")
