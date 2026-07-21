# My Notes

My Notes is an app made by BentleyRR, as a simple lil notes app!

## AI Notice

This project was developed with the assistance of AI. All generated code has been reviewed, modified, and integrated as part of the development process.

## Requirements

* [Python 3.10 or newer](https://www.python.org/downloads)
* [pip](https://pypi.org/project/pip/)
* [Git](https://github.com/git-guides/install-git) (if cloning the repo)


## Clone the Repository

```bash
git clone https://github.com/bentleyrr-official/my-notes.git
cd my-notes
```

## Running

Run the application directly from the project root:

```bash
python main.py
```

## Building

This project can be packaged into a standalone executable using PyInstaller.

Install [PyInstaller](https://github.com/pyinstaller/pyinstaller):

```bash
pip install pyinstaller
```

Build the application:

```bash
pyinstaller --clean --onefile --noconsole --icon="My Notes.ico" --add-data "notes_ui.html;." main.py
```

The compiled executable will be placed in:

```text
dist/
```
