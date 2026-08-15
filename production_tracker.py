"""
Task List Prototype
--------------------
A PyQt5 desktop app that displays a list of TaskItems (Name, Artist, Due Date,
Status) as rectangular cards inside a MainWindow, with a drop-down menu to
sort by Due Date or Status.

Run:
    pip install PyQt5
    python production_tracker.py
"""

import json
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QColor,
    QStandardItem,
)
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
STATUSES = ["Ready", "In Progress", "Review", "Complete"]

TASKS_FILE = Path(__file__).with_name("tasks.json")

# Color used for the left accent bar / border, keyed by status
STATUS_COLORS = {
    "Ready": "#9e9e9e", # grey
    "In Progress": "#f5a623", # orange
    "Review": "#2776f5", # blue
    "Complete": "#4caf50", # green
}

@dataclass
class TaskItem:
    name: str
    artist: str
    due_date: date
    priority: str # "Urgent" | "High" | "Medium" | "Low"
    status: str  # "Ready" | "In Progress" | "Review" | "Complete"

    def to_dict(self):
        d = asdict(self)
        d["due_date"] = self.due_date.isoformat()
        return d

    @staticmethod
    def from_dict(d):
        return TaskItem(
            name=d["name"],
            artist=d["artist"],
            due_date=date.fromisoformat(d["due_date"]),
            priority=d["priority"],
            status=d["status"],
        )

# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
def sample_tasks():
    return [
        TaskItem("Album Cover Art", "J. Rivera", date(2026, 8, 20), "High", "In Progress"),
        TaskItem("Logo Redesign", "M. Chen", date(2026, 8, 15), "Medium", "Ready"),
        TaskItem("Poster Series", "A. Novak", date(2026, 9, 1), "Low", "Ready"),
        TaskItem("Character Sheet", "T. Osei", date(2026, 8, 12), "Urgent", "Review"),
        TaskItem("Storyboard Draft", "L. Fontaine", date(2026, 8, 18), "Low", "In Progress"),
        TaskItem("Book Cover", "S. Patel", date(2026, 8, 30), "Medium", "In Progress"),
        TaskItem("Character Sheet", "T. Osei", date(2026, 7, 12), "High", "Complete"),
        TaskItem("Storyboard Draft", "L. Fontaine", date(2026, 7, 18), "Low", "Review"),
        TaskItem("Book Cover", "S. Patel", date(2026, 7, 30), "Urgent", "Complete"),
    ]

def load_tasks():
    """Load tasks from TASKS_FILE. If it doesn't exist (or is invalid),
    fall back to sample data and write it out so the file exists going forward."""
    if TASKS_FILE.exists():
        try:
            raw = json.loads(TASKS_FILE.read_text())
            return [TaskItem.from_dict(d) for d in raw]
        except (json.JSONDecodeError, KeyError, ValueError):
            pass  # fall through to sample data on corrupt/invalid file
    tasks = sample_tasks()
    save_tasks(tasks)
    return tasks


def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps([t.to_dict() for t in tasks], indent=2))

# ---------------------------------------------------------------------------
# TaskItem widget: a rectangle showing Name, Artist, Due Date, Status
# ---------------------------------------------------------------------------

class TaskItemWidget(QFrame):
    def __init__(self, task: TaskItem, on_edit, parent=None):
        """on_edit: callback(task) invoked when the user clicks this card."""
        super().__init__(parent)
        self.task = task
        self.on_edit = on_edit
        self._build_ui()

    def _build_ui(self):
        self.setObjectName("TaskCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(100)
        self.setCursor(Qt.PointingHandCursor)

        accent = STATUS_COLORS.get(self.task.status, "#9e9e9e")
        self.setStyleSheet(f"""
            #TaskCard {{
                background-color: #2b2b2b;
                border-radius: 8px;
                border-left: 6px solid {accent};
            }}
            #TaskCard:hover {{
                background-color: #333333;
            }}
            QLabel {{
                color: #f0f0f0;
                border: none;
            }}
            QLabel[role="name"] {{
                font-size: 14pt;
                font-weight: 600;
            }}
            QLabel[role="sub"] {{
                color: #b5b5b5;
                font-size: 9pt;
            }}
            QLabel[role="status"] {{
                font-weight: 600;
                color: {accent};
            }}
        """)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        gLayout = QGridLayout()
        gLayout.setContentsMargins(16, 8, 16, 8)

        name_label = QLabel(self.task.name)
        name_label.setProperty("role", "name")

        artist_label = QLabel(f"Artist: {self.task.artist}")
        artist_label.setProperty("role", "sub")

        due_label = QLabel(f"Due: {self.task.due_date.isoformat()}")
        due_label.setProperty("role", "sub")

        status_label = QLabel(self.task.status)
        status_label.setProperty("role", "status")
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        priority_box = QWidget()
        priority_box_layout = QVBoxLayout()
        priority_box.setLayout(priority_box_layout)
        priority_box.setFixedWidth(120)

        priority_label = QLabel(self.task.priority)
        priority_label.setProperty("role", "sub")
        priority_box_layout.addWidget(priority_label)

        gLayout.addWidget(name_label, 0, 0)
        gLayout.addWidget(artist_label, 1, 0)
        gLayout.addWidget(due_label, 1, 1)
        gLayout.addWidget(status_label, 0, 1)
        gLayout.setColumnStretch(0, 3)
        gLayout.setColumnStretch(1, 1)

        mainLayout.addLayout(gLayout)
        mainLayout.addWidget(priority_box)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.on_edit:
            self.on_edit(self.task)
        super().mousePressEvent(event)

# ---------------------------------------------------------------------------
# Edit dialog: change a task's Status and add Notes
# ---------------------------------------------------------------------------

class EditStatusDialog(QDialog):
    def __init__(self, task: TaskItem, parent=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle(f"Edit Task — {task.name}")
        self.setMinimumWidth(750)

        accent = STATUS_COLORS.get(self.task.status, "#9e9e9e")
        self.setStyleSheet(f"""
            QDialog {{ background-color: #2b2b2b; }}
            QLabel {{ color: #f0f0f0; }}
            QPushButton {{ background-color: #3a3a3a; color: #f0f0f0; }}
            QComboBox {{ background-color: #3a3a3a; color: #f0f0f0;
                        padding: 4px 8px; border-radius: 4px; }}
            QComboBox QAbstractItemView {{ background-color: #3a3a3a; color: #f0f0f0; }}
        """)

        layout = QVBoxLayout(self)

        info = QLabel(f"{task.name}  ·  {task.artist}  ·  Due {task.due_date.isoformat()}")
        layout.addWidget(info)

        layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()

        # Color the statuses to match the main UI
        model = self.status_combo.model()
        for i in range(0, len(STATUSES)):
            this_status = STATUSES[i]
            item = QStandardItem(str(this_status))
            item.setForeground(QColor(STATUS_COLORS[this_status]))
            model.appendRow(item)

        self.status_combo.setCurrentText(task.status)

        layout.addWidget(self.status_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_status(self):
        return self.status_combo.currentText()

# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    STATUS_ORDER = {"Ready": 0, "In Progress": 1, "Review": 2, "Complete": 3}
    PRIORITY_ORDER = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 2}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Tracker")
        self.resize(1200, 1200)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.tasks = load_tasks()

        central = QWidget()
        self.setCentralWidget(central)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(16, 16, 16, 16)
        outer_layout.setSpacing(12)

        # --- Sort controls ---
        controls_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("color: #f0f0f0; font-weight: 600;")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Due Date", "Status", "Priority"])
        self.sort_combo.setStyleSheet("""
            QComboBox { background-color: #2b2b2b; color: #f0f0f0;
                        padding: 4px 8px; border-radius: 4px; }
            QComboBox QAbstractItemView { background-color: #2b2b2b; color: #f0f0f0; }
        """)
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)

        controls_layout.addWidget(sort_label)
        controls_layout.addWidget(self.sort_combo)
        controls_layout.addStretch()
        outer_layout.addLayout(controls_layout)

        # --- Scrollable task list ---
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setSpacing(10)
        self.list_layout.addStretch()  # keeps cards top-aligned

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setWidget(self.list_container)
        outer_layout.addWidget(scroll)

        self.render_tasks()

    def on_sort_changed(self, mode: str):
        sorted_tasks = self.tasks
        match mode:
            case "Due Date":
                sorted_tasks = sorted(self.tasks, key=lambda t: t.due_date)
            case "Status":
                sorted_tasks = sorted(
                    self.tasks, key=lambda t: self.STATUS_ORDER.get(t.status, 99)
                )
            case "Priority":
                sorted_tasks = sorted(
                    self.tasks, key=lambda t: self.PRIORITY_ORDER.get(t.priority, 99)
                )
            case _:
                # this is an error
                printf("ERROR: No sort specified")

        self.tasks = sorted_tasks
        self.render_tasks() # re-render after sort

    def render_tasks(self):
        # Clear existing cards (leave the trailing stretch in place)
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for task in self.tasks:
            card = TaskItemWidget(task, on_edit=self.open_edit_dialog)
            self.list_layout.insertWidget(self.list_layout.count() - 1, card)

    def open_edit_dialog(self, task: TaskItem):
        dialog = EditStatusDialog(task, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            new_status = dialog.selected_status()
            if new_status != task.status:
                task.status = new_status
                try:
                    save_tasks(self.tasks)
                except OSError as e:
                    QMessageBox.warning(self, "Save failed", f"Could not save tasks.json:\n{e}")
                self.render_tasks()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()