# Lab0

Lab0 from MLOps subject

# Overview

This project is part of the Fundamentals of Continuous Integration (CI) assignment.
Its goal is to introduce the key components of CI pipelines by developing a Python project that demonstrates linting, automatic code formatting, and testing using modern tools and best practices in MLOps.

The project implements a set of data preprocessing functionalities and exposes them through a Command Line Interface (CLI) built with Click.
All development and testing are performed within an isolated virtual environment managed by uv.

# Structure
```bash
Lab0/
│
├── src/
│   ├── preprocessing.py     # Core data preprocessing functionalities
│   ├── cli.py               # Command Line Interface (CLI) using Click
│
├── tests/
│   ├── test_preprocessing.py  # Unit tests for preprocessing logic
│   ├── test_cli.py            # Integration tests for CLI commands
│
├── pyproject.toml           # Project configuration (dependencies, tools)
├── README.md                # Project documentation
└── .gitignore               # Files and folders to ignore in Git
```

