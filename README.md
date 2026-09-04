# cli-helper-90

`cli-helper-90` is a lightweight Python toolkit designed to streamline the development of robust command-line interfaces. It abstracts complex argument parsing and color formatting into a clean, developer-friendly API.

### Features
*   **Intuitive Command Routing:** Simplify subcommand registration using intuitive function decorators.
*   **Built-in Terminal UI:** Includes pre-configured templates for progress bars, spinners, and formatted table outputs.
*   **Auto-Generated Documentation:** Automatically extracts docstrings to produce clean `--help` menus for your end-users.
*   **Environment Integration:** Native support for loading configuration from `.env` files with a single method call.

### Installation

Install `cli-helper-90` directly from PyPI:

```bash
pip install cli-helper-90
```

To include optional aesthetic dependencies, use:

```bash
pip install cli-helper-90[ui]
```

### Basic Usage

Define your CLI tools with minimal boilerplate using the `CommandGroup` class:

```python
from cli_helper import CommandGroup

cli = CommandGroup(name="app", version="1.0.0")

@cli.command(help="Greet the user")
def greet(name: str):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    cli.run()
```

Run your new CLI tool from the terminal:

```bash
python app.py greet --name "Developer"
# Output: Hello, Developer!
```

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License. See the `LICENSE` file for details.