# Contributing to Greenova

<<<<<<< HEAD
Thank you for your interest in contributing to Greenova! This document provides
guidelines and workflows to help make the contribution process straightforward
and effective.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment Setup](#development-environment-setup)
- [How to Contribute](#how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Feature Requests](#feature-requests)
  - [Documentation Updates](#documentation-updates)
  - [Code Contributions](#code-contributions)
- [Development Workflow](#development-workflow)
  - [Fork-Based Contribution](#fork-based-contribution)
  - [Git Workflow for Direct Contributors](#git-workflow-for-direct-contributors)
  - [Branch Strategy](#branch-strategy)
  - [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
  - [Pull Request Checklist](#pull-request-checklist)
  - [Code Review Process](#code-review-process)
- [Coding Standards](#coding-standards)
  - [Python Code Style](#python-code-style)
  - [HTML/CSS Guidelines](#htmlcss-guidelines)
  - [JavaScript Standards](#javascript-standards)
  - [Testing Requirements](#testing-requirements)
  - [Documentation Requirements](#documentation-requirements)
- [Project Structure](#project-structure)
- [Community](#community)
  - [Getting Help](#getting-help)

## Code of Conduct

Our project adheres to a code of conduct that all contributors are expected to
follow. By participating, you are expected to uphold this code. Please report
unacceptable behavior to the project maintainers.
=======
This document outlines the recommended git workflow for integrating feature
branches into the main branch.

## Overview

The process follows these steps:

1. Update main branch to the latest version
2. Squash and merge the feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

- Appropriate permissions to push to the main branch
- Completed and tested feature in a separate branch
- Understanding of git commands and conflict resolution

## Important Notes

- Always ensure your feature is fully tested before merging
- The squash merge creates a single commit from all changes in the feature
  branch
- This workflow keeps the commit history clean and linear
- Make sure the feature branch is no longer needed before deletion

## After Completion

Once completed, the feature's changes will be integrated into the main branch
as a single commit, and the feature branch will be removed from both local and
remote repositories.
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

We value respect, inclusivity, and a collaborative environment where everyone
feels welcome to contribute.

<<<<<<< HEAD
## Getting Started

### Development Environment Setup
=======
Thank you for contributing to our project! This document outlines our git
workflow for integrating feature branches into the main branch.

## Project Status

Current release: v0.0.4 Next pre-release branch: pre-release/v0.0.4
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

1. **Prerequisites**:

<<<<<<< HEAD
   - Python 3.9.21
   - Node.js 18.20.7
   - NPM 10.8.2
   - Git
=======
For contributors working with a forked repository, follow these steps to avoid
divergent branches and ensure smooth integration:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

2. **Clone the repository** (if you're a direct contributor) or fork it first
   (recommended for external contributors):

   ```bash
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

3. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

The application will be available at
[http://localhost:8000](http://localhost:8000).

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the
   [GitHub Issues](https://github.com/enssol/greenova/issues)
2. If not, [create a new issue](https://github.com/enssol/greenova/issues/new)
   with:
   - A clear, descriptive title
   - Detailed steps to reproduce (for bugs)
   - Expected and actual behavior
   - Screenshots if applicable
   - Your environment details (OS, browser, etc.)

### Feature Requests

For feature requests:

1. Describe the feature in detail
2. Explain the use case and benefits
3. Indicate if you're willing to contribute the feature yourself

### Documentation Updates

Documentation improvements are always welcome:

- Fix typos or clarify existing content
- Add missing information
- Update documentation to reflect current functionality

### Code Contributions

For code contributions, please follow our
[Development Workflow](#development-workflow).

## Development Workflow

We use a fork-based workflow for external contributors and a feature branch
workflow for direct contributors.

### Fork-Based Contribution

For external contributors:

1. **Fork the repository** on GitHub
2. **Clone your fork**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/greenova.git
   cd greenova
   ```

3. **Add upstream remote**:

   ```bash
   git remote add upstream https://github.com/enssol/greenova.git
   ```

4. **Keep your fork updated**:

<<<<<<< HEAD
=======
1. Always sync your fork with upstream before starting new work:

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   ```bash
   git fetch upstream
   git checkout main
   git reset --hard upstream/main
   git push origin main
   ```

<<<<<<< HEAD
5. **Create a feature branch**:
=======
2. Create a feature branch for your work:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

   ```bash
   git checkout -b feature-name
   ```

<<<<<<< HEAD
6. **Make your changes** and commit with
   [proper commit messages](#commit-message-guidelines)

7. **Keep your branch updated** during development:

=======
3. Make your changes and commit frequently with meaningful messages:

   ```bash
   git commit -m "feat: descriptive message about the change"
   ```

4. Keep your branch up to date with upstream:

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   ```bash
   git fetch upstream
   git rebase upstream/main
   # Resolve any conflicts
   ```

8. **Push your changes** to your fork:

   ```bash
   git push origin feature-name
   ```

9. **Create a pull request**:
   - Ensure your branch is up to date with upstream
   - Submit the pull request through GitHub

### Git Workflow for Direct Contributors

For direct contributors:

1. **Update your main branch**:

<<<<<<< HEAD
   ```bash
=======
1. Before submitting a PR, ensure your branch is up to date:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Resolve any conflicts and test your changes thoroughly

3. Push your updated branch to your fork:

   ```bash
   git push origin feature-branch --force-with-lease
   ```

4. Create a pull request through GitHub interface

5. Respond to code review feedback by making additional commits to your branch

### After Your PR is Merged

1. Delete your local feature branch:

   ```bash
   git branch -D feature-branch
   ```

2. Delete the remote branch on your fork:

   ```bash
   git push origin --delete feature-branch
   ```

3. Sync your fork with the updated upstream:
   ```bash
   git fetch upstream
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch**:

   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes** and commit with
   [proper commit messages](#commit-message-guidelines)

4. **Squash and merge your feature branch**:

   ```bash
   git checkout main
   git merge --squash feature-name
   git commit -m "feat: squashed commit message"
   ```

5. **Push changes to main**:

   ```bash
   git push origin main
   ```

6. **Delete the feature branch**:

<<<<<<< HEAD
=======
- Sync your fork with upstream at least weekly
- Don't let branches diverge more than 10 commits
- Keep feature branches short-lived (< 2 weeks)
- Use `git pull --rebase` instead of regular `git pull`
- Consider a monthly "deep cleaning":
  ```bash
  git reflog expire --expire=30.days --all
  git gc --aggressive --prune=now
  ```

## Git Workflow Overview (Direct Contributors)

Our integration process follows these key steps:

1. Update your main branch to the latest version
2. Squash and merge your feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

Before you begin:

- Ensure you have appropriate permissions to push to the main branch
- Complete and thoroughly test your feature in a separate branch
- Be familiar with git commands and conflict resolution

## Step-by-Step Process

# 1. Switch to main and get latest changes

`git checkout main` `git pull origin main`

# 2. Squash and merge the feature branch (resolve any conflicts if they arise)

`git merge --squash feature-branch`
`git commit -m "feat: squashed commit message"`

# 3. Push changes to main

`git push origin main`

# 4. Delete feature branch locally

`git branch -D feature-branch`

# 5. Delete feature branch remotely

`git push origin --delete feature-branch`

# Note: Ensure the feature branch is no longer needed before deleting it remotely.

## Conflict Resolution Guidelines

If you encounter merge conflicts:

1. Understand both sides of the conflict before resolving
2. When in doubt, consult with team members familiar with the code
3. For complex conflicts, consider using a visual merge tool:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   ```bash
   git branch -D feature-name
   git push origin --delete feature-name
   ```

### Branch Strategy

<<<<<<< HEAD
- Use `main` for production-ready code
- Use `pre-release` branches for upcoming releases
- Use feature branches for new features or bug fixes

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/)
standard:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:

```bash
git commit -m "feat: add user authentication"
```

## Pull Request Process

### Pull Request Checklist

Before submitting a pull request:

1. Ensure your branch is up to date with `main`
2. Run tests and ensure they pass
3. Follow coding standards
4. Provide a clear description of the changes
5. Reference related issues (if any)

### Code Review Process

- Pull requests will be reviewed by maintainers
- Address feedback promptly
- Make additional commits to your branch as needed

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where applicable
- Write docstrings for all functions and classes

### HTML/CSS Guidelines

- Follow [W3C standards](https://www.w3.org/)
- Use semantic HTML
- Keep CSS modular and reusable

### JavaScript Standards

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use ES6+ features
- Write unit tests for all functions

### Testing Requirements

- Write tests for new features and bug fixes
- Use pytest for Python tests
- Use Jest for JavaScript tests

### Documentation Requirements

- Update documentation for new features
- Ensure examples are clear and accurate

## Project Structure

- `src/`: Source code
- `tests/`: Test cases
- `docs/`: Documentation
- `assets/`: Static files (images, CSS, JS)

## Community

### Getting Help

If you need help:

- Check the
  [GitHub Discussions](https://github.com/enssol/greenova/discussions)
- Reach out to maintainers via email
- Join our Slack channel (link available in the repository)

Thank you for contributing to Greenova!
=======
If you encounter any issues with the git workflow, please reach out to the team
lead or open a discussion on GitHub.
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
