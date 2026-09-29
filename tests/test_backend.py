import tempfile
import unittest
from pathlib import Path
from backend import TaskStore


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'tasks.sqlite3'
        self.store = TaskStore(self.path)

    def test_interfaces_share_persistent_changes(self):
        other = TaskStore(self.path)
        task_id = self.store.add('  Finish lab  ')
        self.assertEqual(other.list_tasks(), [(task_id, 'Finish lab', 0)])
        other.toggle(task_id)
        self.assertEqual(self.store.list_tasks(), [(task_id, 'Finish lab', 1)])
        self.store.toggle(task_id)
        self.assertEqual(other.list_tasks()[0][2], 0)
        other.delete(task_id)
        self.assertEqual(TaskStore(self.path).list_tasks(), [])

    def test_invalid_titles_are_not_saved(self):
        for title in ['', '   ', 'x' * 201]:
            with self.assertRaises(ValueError):
                self.store.add(title)
        self.assertEqual(self.store.list_tasks(), [])

    def test_titles_are_stored_as_data(self):
        title = "Read 'SQL'; DROP TABLE tasks; -- ✓"
        self.store.add(title)
        self.assertEqual(self.store.list_tasks()[0][1], title)
        self.store.add('Still works')
        self.assertEqual(len(self.store.list_tasks()), 2)


if __name__ == '__main__':
    unittest.main()
