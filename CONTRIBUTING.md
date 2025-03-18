# Contributing to Meeting Assistant

Thank you for your interest in contributing to the Meeting Assistant project! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots and animated GIFs if possible
* Include error messages and stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful
* List some other applications where this enhancement exists, if applicable

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Make your changes
5. Run tests and ensure they pass:
   ```bash
   pytest --cov=./ --cov-report=term-missing
   ```
6. Format your code:
   ```bash
   black .
   isort .
   flake8 .
   ```
7. Commit your changes:
   ```bash
   git commit -am 'Add amazing feature'
   ```
8. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
9. Submit a pull request

## Style Guide

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [Black](https://github.com/psf/black) for code formatting
* Use [isort](https://pycqa.github.io/isort/) for import sorting
* Use [flake8](https://flake8.pycqa.org/) for style guide enforcement

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Documentation

* Use docstrings for all public modules, functions, classes, and methods
* Follow the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html) for docstrings
* Keep README.md and other documentation up to date

## Additional Notes

### Issue and Pull Request Labels

* `bug`: Something isn't working
* `enhancement`: New feature or request
* `documentation`: Improvements or additions to documentation
* `good first issue`: Good for newcomers
* `help wanted`: Extra attention is needed
* `question`: Further information is requested

## Recognition

Contributors who have their PRs merged will be added to the README.md file in the Contributors section.

Thank you for contributing to Meeting Assistant! 