# brew-dependency-submission-action

Brew Lockfile Dependency Submission Action

## Usage

```yaml
- name: Brew Lockfile Dependency Submission Action
  uses: GeekMasher/brew-dependency-submission-action@main
  with:
    # [optonal] The path to the Brewfile.lock.json file. Defaults to finding all Brewfile.lock.json in the current
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
        uses: GeekMasher/brew-dependency-submission-action@main
```


