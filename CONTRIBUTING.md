# Contributing to Brew Dependencies Submission Action

## Getting Started

This project uses the following tools for development:

- [Python +3.9](https://www.python.org/downloads/)
- [`uv`](https://docs.astral.sh/uv/)

You need to do the following steps before you can start contributing to this repository.

- [Fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- Run tests
- Run linting / formatting
- Run vendoring script

### Running Tests

You need to run all the tests before submitting a PR.

```bash
uv run python -m unittest discover -v -s ./tests -p 'test_*.py'"
```

### Formatting

This project uses `black` for code formatting. You can run the following command to format your code before submitting a PR.

```bash
uv run black ./bldsa
```

You can also run the following command to check if your code is formatted correctly.

```bash
black --check ./bldsa
```

### Vendoring Dependencies

This project uses a `update.sh` script to vendor dependencies. You can run the following command to vendor dependencies.

```bash
./vendor/update.sh
```
