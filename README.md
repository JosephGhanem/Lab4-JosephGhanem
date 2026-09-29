# Lab 4 — Git and GitHub (Solo)

A Python task manager with two desktop interfaces: Tkinter and PyQt6. Both use
one SQLite backend, so a task created in either interface is available in the
other. This project follows the solo workflow in **Lab 4-Git.docx**.

## Setup and run

Use Python 3.10 or newer with Tkinter installed. From this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py --ui tkinter
python main.py --ui pyqt
```

On Windows, activate with `.venv\Scripts\activate` instead. On this Mac, the
prepared environment can be used directly:

```sh
.venv/bin/python main.py --ui tkinter
.venv/bin/python main.py --ui pyqt
```

Close the first window before running the second command, or use two terminals
to open both. Each toolkit runs in its own process with its own event loop.

## Using the application

Enter a title and click **Add task** (or press Enter). Select a task and click
**Toggle complete** to change its status. **Delete** asks for confirmation.
**Refresh** reloads saved tasks, including changes made by the other interface.
Blank titles and titles longer than 200 characters are rejected.

Data is automatically saved in `data/tasks.sqlite3`, relative to the project,
regardless of the terminal's working directory. Local task data is excluded from
Git. An alternative database can be selected with `--db /path/to/tasks.sqlite3`;
both interfaces must use the same path to share tasks.

## Project structure

- `main.py`: command-line launcher and interface selection.
- `backend.py`: shared validation and SQLite operations.
- `tkinter_ui.py`: Tkinter/ttk interface.
- `pyqt_ui.py`: PyQt6 interface.
- `tests/test_backend.py`: persistence, validation, and SQL safety tests.
- `tests/gui_smoke.py`: integration test using real widgets from both toolkits.
- `requirements.txt`: PyQt dependency; Tkinter comes from the Python installation.

## Testing

```sh
python -m unittest discover -s tests -v
python tests/gui_smoke.py
```

The GUI test needs a desktop session and both GUI toolkits. It uses a temporary
database and does not modify personal tasks. It creates a task through Tkinter,
reads and completes it through PyQt, refreshes Tkinter, adds another task through
PyQt, deletes a task, and checks blank-title validation.

Manual demonstration:

1. Open Tkinter and add `Finish Lab 4`.
2. Open PyQt using the same database; verify the task appears.
3. Mark the task complete in PyQt.
4. Click Refresh in Tkinter; verify it shows Complete.
5. Restart either interface; verify the saved task remains.
6. Delete the task and refresh the other interface; verify it disappears.

## Solo Git workflow

Work is kept on `main`. The assignment's solo section does not require a second
student, feature branches, pull requests, merges, or a “who pushed what” file.
The local commit author is a neutral workspace identity until the student's Git
identity is supplied; it does not identify a second contributor.

To inspect the work:

```sh
git status
git log --oneline
git show v1.0 --stat
```

To make further changes:

```sh
git add main.py backend.py tkinter_ui.py pyqt_ui.py README.md tests
git commit -m "Describe the change"
git push origin main
```

## GitHub and submission — still to complete

The project has been prepared locally. No GitHub repository, invitation,
GitHub release, or Moodle submission has been created by this local setup.

1. Set your identity: `git config user.name "Your Full Name"` and
   `git config user.email "Your GitHub email or noreply address"`.
2. Create an empty GitHub repository named `Lab4-YourFullName`. Use private
   visibility if required. Do not initialize the remote with another README.
3. Connect and push (replace the example URL with your repository URL):

   ```sh
   git remote add origin https://github.com/YOUR_USERNAME/Lab4-YourFullName.git
   git push -u origin main
   git push origin v1.0
   ```

4. If private, add the instructor and TAs using their actual GitHub usernames.
5. Optionally create a GitHub release for the `v1.0` tag.
6. Submit the repository URL and this README on Moodle. No contribution-tracking
   document is needed for a solo submission.

The assignment also asks the student to review its Git tutorial and VS Code
source-control exercise. Reading and personal practice are not represented as
completed by this project.

## References

- Assignment: `Lab 4-Git.docx`, especially the solo-project section.
- Git tutorial: https://www.w3schools.com/git/
- VS Code source control: https://code.visualstudio.com/docs/sourcecontrol/overview
- Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- PyQt6 documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/

## Verification results

Verified locally on macOS with Python 3.13, PyQt6 6.11.0, and Tk 9.0:

- All three backend tests passed.
- The real-widget Tkinter/PyQt integration smoke test passed.
- The launcher help command passed.

The missing Tkinter component was installed through Homebrew
(`brew install python-tk@3.13`), which also upgraded Python 3.13 and required
Homebrew dependencies. The project's PyQt installation is isolated in `.venv`.
The GUI smoke test requires access to the desktop window system; a sandboxed
run without that access may abort before displaying a window.
