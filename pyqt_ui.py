"""PyQt6 view of the same task manager and database."""
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QTreeWidget,
                            QTreeWidgetItem, QMessageBox)
from backend import TaskStore


class TaskWindow(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.setWindowTitle('Lab 4 | Task Manager | PyQt')
        self.resize(720, 460)
        self.setMinimumSize(540, 350)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        heading = QLabel('My tasks')
        heading.setStyleSheet('font-size: 24px; font-weight: bold;')
        layout.addWidget(heading)
        layout.addWidget(QLabel('PyQt interface • Shared local task database'))
        entry_row = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setPlaceholderText('Enter a task title')
        self.entry.returnPressed.connect(self.add)
        entry_row.addWidget(self.entry)
        add_button = QPushButton('Add task')
        add_button.clicked.connect(self.add)
        entry_row.addWidget(add_button)
        layout.addLayout(entry_row)
        self.table = QTreeWidget()
        self.table.setHeaderLabels(['Task', 'Status'])
        self.table.setRootIsDecorated(False)
        self.table.setColumnWidth(0, 480)
        layout.addWidget(self.table)
        actions = QHBoxLayout()
        for label, callback in [('Toggle complete', lambda: self.change('toggle')),
                                ('Delete', lambda: self.change('delete')),
                                ('Refresh', self.refresh)]:
            button = QPushButton(label)
            button.clicked.connect(callback)
            actions.addWidget(button)
        layout.addLayout(actions)
        self.status = QLabel()
        layout.addWidget(self.status)
        self.refresh()

    def refresh(self):
        try:
            rows = self.store.list_tasks()
        except sqlite3.Error as error:
            QMessageBox.critical(self, 'Storage error', str(error))
            return
        self.table.clear()
        for task_id, title, done in rows:
            item = QTreeWidgetItem([title, 'Complete' if done else 'To do'])
            item.setData(0, Qt.ItemDataRole.UserRole, task_id)
            self.table.addTopLevelItem(item)
        self.status.setText(f'{len(rows)} tasks • {sum(row[2] for row in rows)} complete')

    def add(self):
        try:
            self.store.add(self.entry.text())
        except (ValueError, sqlite3.Error) as error:
            QMessageBox.warning(self, 'Cannot add task', str(error))
            return
        self.entry.clear()
        self.refresh()

    def change(self, action):
        item = self.table.currentItem()
        if item is None:
            QMessageBox.information(self, 'Select a task', 'Select a task first.')
            return
        if action == 'delete' and QMessageBox.question(self, 'Delete task', 'Delete the selected task?') != QMessageBox.StandardButton.Yes:
            return
        try:
            getattr(self.store, action)(item.data(0, Qt.ItemDataRole.UserRole))
        except sqlite3.Error as error:
            QMessageBox.critical(self, 'Storage error', str(error))
        self.refresh()


def run(path):
    app = QApplication([])
    window = TaskWindow(TaskStore(path))
    window.show()
    app.exec()
