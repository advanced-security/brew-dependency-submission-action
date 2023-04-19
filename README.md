# brew-dependency-submission-action

Brew Lockfile Dependency Submission Action

## Usage

```yaml
- name: Brew Lockfile Dependency Submission Action
  uses: advanced-security/brew-dependency-submission-action@main
  with:
    # [optonal] The path to the gradle.lock file. Defaults to finding all gradle*.lock in the current
    # working directory
    brew-lock: "./Brewfile.lock.json"
    # [optional ] Token used to authenticate with the GitHub API. Defaults to the GITHUB_TOKEN secret.
    token: ${{ secrets.ACTIONS_TOKEN }}
```

#### Workflow Example

```yaml
name: Brew Lockfile Dependency Submission Action
on:
  push:
    branches: [main]

permissions: 
  contents: write   # needed

jobs:
  gradle-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # ... generate Brew lockfile

      - name: Brew Lockfile Dependency Submission Action
        uses: advanced-security/brew-dependency-submission-action@main
```


## License 

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE) for the full terms.


## Maintainers 

Maintained by [@GeekMasher](https://github.com/GeekMasher).


## Support

Please [create GitHub issues](https://github.com/advanced-security/brew-dependency-submission-action) for any feature requests, bugs, or documentation problems.


## Acknowledgement

- @GeekMasher: Author and Maintainer

