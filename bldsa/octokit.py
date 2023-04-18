from typing import *

import requests


class Octokit:
    def __init__(self, owner: str, repo: str, token: str, url="https://api.github.com"):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.url = url

    def submitDependencies(self, dependencies: dict):
        """Submit dependencies to GitHub

        https://docs.github.com/en/enterprise-cloud@latest/rest/dependency-graph/dependency-submission?apiVersion=2022-11-28#create-a-snapshot-of-dependencies-for-a-repository
        """
        url = f"{self.url}/repos/{self.owner}/{self.repo}/dependency-graph/snapshots"
        resp = requests.post(
            url,
            json=dependencies,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {self.token}",
            },
        )

        if resp.status_code != 201:
            raise Exception(
                f"Failed to submit dependencies: {resp.status_code} {resp.text}"
            )
