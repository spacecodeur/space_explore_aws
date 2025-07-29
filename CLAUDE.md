# Space Explore AWS

## Project Overview

This is a comprehensive AWS learning workspace designed for hands-on experimentation and certification preparation. The project currently centers around a custom command management system that simplifies AWS CLI and related tool usage, but is architected to expand into a complete learning ecosystem.

The command system allows creating "human-friendly" commands that point to real technical commands (AWS CLI, Terraform, CDK, etc.), making it easier to learn and practice AWS operations while building a personal reference library.

## Architecture

### Main file
- `cli.py` : Main Python script that handles command execution

### Folder structure
- `commands/` : Folder containing all command definitions in JSON format
  - Supports subfolders to organize commands by service/category/tool
  - Example: `commands/s3/`, `commands/terraform/`, `commands/cdk/`, etc.

## Features

### 1. JSON-based command definitions
Each command is defined in a JSON file with the following structure:
```json
{
    "description": "Command description",
    "parameters": [
        {
            "name": "param_name",
            "description": "Parameter description"
        }
    ],
    "command": "any_command with variables $1 $2 $n",
    "example": "usage example"
}
```

### 2. Variable system
- Dynamic variables: `$1`, `$2`, `$n` in the `command` field
- Automatic parameter substitution during execution
- All parameters are mandatory (no optional parameters)

### 3. Usage modes

#### List mode
```bash
python3 cli.py
```
Displays all available commands with their full paths

#### Help mode
```bash
python3 cli.py commands/command_name.json -h
```
Shows detailed help: description, parameters, example, technical command

#### Execution mode
```bash
python3 cli.py commands/command_name.json param1 param2
```
Executes the command with variable substitution

## Command examples

### AWS CLI commands
- S3 operations: copy files, list buckets
- EC2 operations: instance management
- IAM operations: user/role management

### Potential other tools
- **Terraform**: Infrastructure as Code commands
- **AWS CDK**: Cloud Development Kit commands
- **CloudFormation**: Stack management commands
- **Docker**: Container management for AWS services
- **kubectl**: Kubernetes commands for EKS

## Learning objectives

- **AWS certifications preparation** (Solutions Architect, Developer, SysOps, etc.)
- **Hands-on AWS experience** through practical command execution
- **Command-line tools mastery** for AWS CLI, Terraform, CDK, and related tools
- **Knowledge organization** by AWS service, tool, and learning concept
- **Personal reference library** creation for quick access to common operations
- **Best practices documentation** and real-world scenario practice
- **Future expansion** to include tutorials, containers, and comprehensive learning materials

## Technologies used

- **Python 3**: Main language
- **JSON**: Command definition format
- **subprocess**: System command execution
- **Generic design**: Supports any command-line tool

## Auto-completion

The system supports auto-completion with [Tab] after `python3 cli.py ` to navigate through the command file tree.

## Git Hooks

The project includes Git hooks in the `.git-hooks/` folder to enforce code quality:

### Pre-commit Hook (`pre-commit`)
- Validates branch naming convention: `<prefix>/branch-name`
- Allowed prefixes: `feature`, `fix`, `chore`, `docs`, `test`, `refactor`, `poc`
- Examples: `feature/user-authentication`, `fix/navbar-alignment`

### Commit Message Hook (`commit-msg`)
- Enforces commit message format: `type: subject`
- Allowed types: `feature`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`, `ci`
- Examples: `feature: add user login flow`, `fix: handle null values in API response`

To activate the hooks, configure Git to use the `.git-hooks/` directory:
```bash
git config core.hooksPath .git-hooks
```

## Important notes

- **Generic system**: Can handle any command-line tool, not just AWS CLI
- **Flexible organization**: Subfolders supported for organizing by tool/service
- **Automatic validation**: Parameter count verification
- **Automatic help display**: Shows help on parameter errors
- **Extensible**: Easy to add new tools and commands
- **Learning-focused**: Designed for certification preparation and skill building