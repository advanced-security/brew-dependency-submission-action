# brew-dependency-submission-action

This is the [Brew / Homebrew Dependency Submission Action](https://github.com/advanced-security/brew-dependency-submission-action) which parses Homebrew files and submits the dependencies to the [Dependency Graph Submission API](https://docs.github.com/en/enterprise-cloud@latest/code-security/supply-chain-security/understanding-your-software-supply-chain/using-the-dependency-submission-api).

This means thats [GitHub's Dependabot](https://docs.github.com/en/enterprise-cloud@latest/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) can use the Homebrew to check for security vulnerabilities in your dependencies and keeping your Software Bill of Materials up to date.

## Usage

```yaml
- name: Brew Lockfile Dependency Submission Action
  uses: advanced-security/brew-dependency-submission-action@v1
```

### Action Inputs

```yaml
- name: Brew Lockfile Dependency Submission Action
  uses: advanced-security/brew-dependency-submission-action@v1
  with:
    # [optonal] The path to the Brewfile.lock.json file. Defaults to finding all Brewfile.lock.json in the current
    # working directory
    brew-lock: "./Brewfile.lock.json"
    # [optional] Token used to authenticate with the GitHub API. Defaults to the GITHUB_TOKEN secret.
    token: ${{ secrets.ACTIONS_TOKEN }}
```

### Workflow Example

```yaml
name: Brew Lockfile Dependency Submission Action
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions: 
  contents: write   # needed

jobs:
  gradle-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # ... generate Brew lockfile

      - name: Brew Lockfile Dependency Submission Action
        uses: advanced-security/brew-dependency-submission-action@v1
```


## License 

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE) for the full terms.


## Maintainers 

Maintained by [@GeekMasher](https://github.com/GeekMasher).


## Support

Please [create GitHub issues](https://github.com/advanced-security/brew-dependency-submission-action) for any feature requests, bugs, or documentation problems.


## Acknowledgement

- @GeekMasher: Author and Maintainer
