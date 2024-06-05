# Contributing to Mooover Backend

Thank you for considering contributing to the Mooover backend! We welcome contributions from the community to help improve this project. Please follow these guidelines to ensure a smooth and effective collaboration.

## Table of Contents

- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [License](#license)

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following details:

- A clear and descriptive title.
- A detailed description of the issue and steps to reproduce.
- Any relevant logs or screenshots.
- The expected and actual behavior.
- Use the labels to tag the issue accordingly.

### Suggesting Enhancements

We welcome suggestions for new features or enhancements. To suggest an enhancement:

- Check the existing issues to see if your idea has already been suggested.
- If not, create a new issue with a clear and descriptive title.
- Provide a detailed description of the enhancement and its benefits.
- Include any relevant examples or mockups.
- Use the labels to tag the issue accordingly.

### Submitting Pull Requests

To contribute code changes:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, following the [coding guidelines](#coding-guidelines).
4. Commit your changes with a descriptive message (see [commit messages](#commit-messages)).
5. Push your branch to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a pull request on the main repository.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adipopbv/mooover-backend.git
   cd mooover-backend
   ```

2. **Install dependencies:**

   It's recommended to use a virtual environment **for each** service:
   ```bash
   cd services/?-services   # Replace ? with the service name
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   pip install -e ../../corelib   # The commons library installed as editable
   ```

3. **Set up environment variables:**
   Modify the `.config` file with the necessary values as described in the main [README](README.md).

4. **Run the services locally:**  
   Using docker:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```   

## Coding Guidelines

To maintain consistency and quality in the Mooover backend project, please follow these coding guidelines when contributing.

### General Principles

- **Readability:** Write code that is easy to read and understand.
- **Simplicity:** Keep your code as simple as possible.
- **Consistency:** Follow the project's coding style and conventions.
- **Modularity:** Write modular and reusable code.

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/), the official Python style guide.
- Use meaningful variable and function names.
- Keep functions short and focused on a single task.
- Use type hints for function signatures.
- Handle exceptions appropriately and avoid using bare `except` clauses.

### Documentation

- Write docstrings for all public modules, classes, and functions.
- Document any important decisions or architectural patterns in the code.

### Testing

- Write unit tests for all new features and bug fixes (if possible).
- Use [pytest](https://docs.pytest.org/en/stable/) as the testing framework.
- Ensure all tests pass before submitting a pull request.
- Aim for high test coverage but do not sacrifice code quality for coverage.

## Commit Messages

- Use the past tense ("Added feature").
- Keep the first line under 50 characters.
- Include a detailed description of the change if necessary.

## License

By contributing, you agree that your contributions will be licensed under the BSD-3-Clause License.

---

Thank you for contributing to Mooover Backend!
