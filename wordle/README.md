# Project Python

The purpose of this project is to remake the popular web game, Wordle, in Python.

## Team Information

**Team ID:** team-wordle-fibble-2
**Problem/Project name:** Wordle/Fibble
**Team Name:** Project Python
**Members 4:**

- Colin Murphy (email: cm787623@ohio.edu, gh: https://github.com/Colinster327)
- Brian Hartman (email: bh018420@ohio.edu, gh: https://github.com/bhartman4)
- Aidan Rogers (email: ar320621@ohio.edu, gh: https://github.com/Aidan-Rogers)
- Connor Daggett (email: cd163721@ohio.edu, gh: https://github.com/Cdagg96)

## About this project

We plan to use the python game library, Pygame to complete the project. Overall, this project is split into 4 main
parts. First, to setup all the dependencies and code structure in order to make it easy for multiple people to edit
source code at the same time. Second, all of the visual components must be made. Third, create and implement the
algorithms used to check the word and give feedback to the user. Finally, the code needs to be organized and abstracted
as much as possible to make it efficient and easier to read / edit in the future.

## Platform

Both MacOS and Windows will be used (depending on the person). In addition, Python v3.11+ will be the language used.

## Frameworks/Tools

Frameworks or tools include Visual Studio Code, Git, Python, Pip, and Pygame.

## Initial Requirements

- Python: version 3.11
- Pip: greater than version 20.0.0
- Git: most recent version

## How to build/compile

- Clone the repository with `git clone ${repo-link}`
- Create a Virtual Environment with `python -m venv venv` (this is used for python dependency managing)
- Enter into the venv on Windows with `venv\Scripts\activate.bat`
- Enter into the venv on MacOS with `source venv/bin/activate`
- Once in the virtual environment, install dependencies with `pip install -r requirements.txt` (make sure you are in the venv!)
- Make sure to run the above command every time you `git pull` the repo!
- To run the game, make sure you are in the s24-wordle-fibble-2 directory and type `make run_local` (make sure you are in the venv!)
- When done, exit the virtual environment by typing `deactivate`

## Common Errors

- If any error arises about `python` or `pip` not existing, try `python3` and / or `pip3` respectively
- If an error arises when trying to run the game, make sure you are in your virtual environment!!

## Pull Requests

- When committing code to the remote repo, make a new branch off of `main`
- When done with changes, commit the code to that branch
- Push the branch to the remote repo and create a Pull Request
- Assign the reviewer to someone other than yourself and wait for it to be approved before merging into `main`

## Recommended Python Formatter

- For VSCode, install and use the `autopep8` extention and keep the indention to the default 4
- You can assign a key stroke to format the file by going to your VSCode settings

## Type Checking

- Having type checking enabled will greatly reduce run time errors by telling before you run the program
- To enable this on VSCode, look at the menu bar on the bottom of the editor, click `{ }` and select `Type Checking    switch to on`
- This will add a .vscode folder to your base directory. This is ok since the folder is on the `.gitignore`

## Adding a dependency

- Use `pip install _____` inside the virtual environment to install the dependency needed
- Add the name and version of the dependency to `requirements.txt`
- An example would be `pygame==2.5.2`

## Documentation

- Make sure doxygen is installed
- Use `make doc` in the root of the repo to generate documentation
- All created documentation will be in the html folder

## Unit Testing

- We use Pytest
- Make sure Pytest is installed with `pip install -r requirements.txt`
- Add tests in the `/test` directory
- The file must include the pattern `test_*.py`
- The functional tests must start with `test_`
- Make sure there is only one file per class
- To run all tests use `make test` in the root directory

## Releases

- We use Pyinstaller to package the game into an executable
- Make sure Pyinstaller is installed with `pip install -r requirments.txt`
- Run the command `make build` on either Mac or Windows to generate either a unix executable or regular executable respectively
- The executable can be found in the `dist` directory as `game` (MacOS) or `game.exe` (Windows)
- To run the executable you just made, use `make run_mac` or `make run_windows`

## Using LLM for Hints

- In order to use an LLM for hints, you must have a vaild openai api key in your `.zshrc`, `.bashrc`, `.profile`, etc...
- For MacOS, you can add `export OPENAI_API_KEY=your-api-key` or `export GEMINI_API_KEY=your-api-key`
- For Windows, you can add `set OPENAI_API_KEY=your-api-key` or `set GEMINI_API_KEY=your-api-key`
- Make sure to restart your terminal after adding the key
- Troubleshooting: visit [Google Gemini](https://ai.google.dev/gemini-api/docs/api-key) or [OpenAI](https://platform.openai.com/docs/quickstart)
