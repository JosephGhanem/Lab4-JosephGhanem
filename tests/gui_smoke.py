"""Run actual GUI callbacks against one temporary database."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from PyQt6.QtWidgets import QApplication, QMessageBox
from unittest.mock import patch
from backend import TaskStore
from tkinter_ui import TaskWindow as TkWindow
from pyqt_ui import TaskWindow as QtWindow

with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / 'shared.sqlite3'
    root = tk.Tk()
    root.withdraw()
    tkinter = TkWindow(root, TaskStore(path))
    tkinter.title.set('Created in Tkinter')
    tkinter.add()
    root.update()
    app = QApplication([])
    qt = QtWindow(TaskStore(path))
    assert qt.table.topLevelItem(0).text(0) == 'Created in Tkinter'
    qt.table.setCurrentItem(qt.table.topLevelItem(0))
    qt.change('toggle')
    tkinter.refresh()
    assert tkinter.table.item(tkinter.table.get_children()[0], 'values')[1] == 'Complete'
    qt.entry.setText('Created in PyQt')
    qt.add()
    tkinter.refresh()
    assert len(tkinter.table.get_children()) == 2
    qt.table.setCurrentItem(qt.table.topLevelItem(0))
    with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Yes):
        qt.change('delete')
    tkinter.refresh()
    assert len(tkinter.table.get_children()) == 1
    with patch('tkinter_ui.messagebox.showerror') as error:
        tkinter.title.set('   ')
        tkinter.add()
        error.assert_called_once()
    qt.show()
    app.processEvents()
    qt.close()
    root.destroy()
print('PASS: Tkinter/PyQt add, shared persistence, toggle, delete, refresh and validation')
