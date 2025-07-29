# Space Explore AWS

A comprehensive learning environment for AWS technologies and cloud computing concepts. This project serves as a hands-on laboratory for AWS certification preparation, experimentation, and skill development.

## Overview

This is a personal AWS learning workspace that evolves with your cloud journey. Currently featuring a custom command management system, but designed to grow into a complete learning ecosystem that may include tutorials, Docker containers for testing, infrastructure as code examples, and more.

## Quick Start

### List all available commands
```bash
python3 cli.py
```

### Get help for a specific command
```bash
python3 cli.py commands/command_name.json -h
```

### Execute a command
```bash
python3 cli.py commands/command_name.json param1 param2
```

## Current Features

### Custom Command System
- **JSON-based command definitions** with parameters and descriptions
- **Auto-completion** support with Tab navigation
- **Flexible organization** using subfolders (s3/, terraform/, cdk/, etc.)
- **Generic design** - works with any command-line tool
- **Learning-focused** for AWS certifications and skill building
- **Git hooks integration** for enforcing code quality standards

### Future Learning Components
This workspace is designed to expand with additional learning materials and tools:
- **Interactive tutorials** and guided exercises
- **Docker containers** for safe AWS service testing
- **Infrastructure as Code** examples (Terraform, CDK, CloudFormation)
- **Certification study guides** and practice scenarios
- **Best practices documentation** and real-world examples

## Command Structure

Commands are defined in JSON files under the `commands/` directory:

```json
{
    "description": "Command description",
    "parameters": [
        {
            "name": "param_name",
            "description": "Parameter description"
        }
    ],
    "command": "aws s3 cp $1 $2",
    "example": "python3 cli.py commands/s3/copy.json file.txt s3://bucket/"
}
```

## Git Hooks

The project includes Git hooks to enforce code quality and consistency:

### Pre-commit Hook
- **Branch naming validation**: Ensures branches follow the naming convention `<prefix>/branch-name`
- **Allowed prefixes**: `feature`, `fix`, `chore`, `docs`, `test`, `refactor`, `poc`
- **Examples**: `feature/user-authentication`, `fix/navbar-alignment`, `docs/project-guidelines`

### Commit Message Hook
- **Message format validation**: Enforces the format `type: subject`
- **Allowed commit types**:
  - `feature`: A new feature
  - `fix`: A bug fix
  - `chore`: Routine task that doesn't affect the code logic
  - `docs`: Documentation-only changes
  - `test`: Adding or updating tests
  - `refactor`: Code change that neither fixes a bug nor adds a feature
  - `perf`: Performance improvement
  - `ci`: Changes to CI/CD configuration or scripts

### Setting up Git Hooks

To activate the hooks after cloning, configure Git to use the `.git-hooks/` directory:

```bash
git config core.hooksPath .git-hooks
```