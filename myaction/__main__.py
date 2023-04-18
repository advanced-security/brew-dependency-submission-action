import os
import argparse

parser = argparse.ArgumentParser(__name__)

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


if __name__ == "__main__":
    arguments = parser.parse_args()

    # My action workflow

