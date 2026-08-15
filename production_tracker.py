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

import sys
from dataclasses import dataclass
from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class TaskItem:
    name: str
    artist: str
    due_date: date
    status: str  # "Not Started" | "In Progress" | "Done"


# Color used for the left accent bar / border, keyed by status
STATUS_COLORS = {
    "Not Started": "#9e9e9e",
    "In Progress": "#f5a623",
    "Done": "#4caf50",
}


def sample_tasks():
    return [
        TaskItem("Album Cover Art", "J. Rivera", date(2026, 8, 20), "In Progress"),
        TaskItem("Logo Redesign", "M. Chen", date(2026, 8, 15), "Not Started"),
        TaskItem("Poster Series", "A. Novak", date(2026, 9, 1), "Not Started"),
        TaskItem("Character Sheet", "T. Osei", date(2026, 8, 12), "Done"),
        TaskItem("Storyboard Draft", "L. Fontaine", date(2026, 8, 18), "In Progress"),
        TaskItem("Book Cover", "S. Patel", date(2026, 8, 30), "Done"),
    ]


# ---------------------------------------------------------------------------
# TaskItem widget: a rectangle showing Name, Artist, Due Date, Status
# ---------------------------------------------------------------------------

class TaskItemWidget(QFrame):
    def __init__(self, task: TaskItem, parent=None):
        super().__init__(parent)
        self.task = task
        self._build_ui()

    def _build_ui(self):
        self.setObjectName("TaskCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(80)

        accent = STATUS_COLORS.get(self.task.status, "#9e9e9e")
        self.setStyleSheet(f"""
            #TaskCard {{
                background-color: #2b2b2b;
                border-radius: 8px;
                border-left: 6px solid {accent};
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

        layout = QGridLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        name_label = QLabel(self.task.name)
        name_label.setProperty("role", "name")

        artist_label = QLabel(f"Artist: {self.task.artist}")
        artist_label.setProperty("role", "sub")

        due_label = QLabel(f"Due: {self.task.due_date.isoformat()}")
        due_label.setProperty("role", "sub")

        status_label = QLabel(self.task.status)
        status_label.setProperty("role", "status")
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(name_label, 0, 0)
        layout.addWidget(artist_label, 1, 0)
        layout.addWidget(due_label, 1, 1)
        layout.addWidget(status_label, 0, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    STATUS_ORDER = {"Not Started": 0, "In Progress": 1, "Done": 2}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task List")
        self.resize(520, 600)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.tasks = sample_tasks()

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
        self.sort_combo.addItems(["Due Date", "Status"])
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

        self.render_tasks(self.tasks)

    def on_sort_changed(self, mode: str):
        if mode == "Due Date":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.due_date)
        else:  # "Status"
            sorted_tasks = sorted(
                self.tasks, key=lambda t: self.STATUS_ORDER.get(t.status, 99)
            )
        self.render_tasks(sorted_tasks)

    def render_tasks(self, tasks):
        # Clear existing cards (leave the trailing stretch in place)
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for task in tasks:
            card = TaskItemWidget(task)
            self.list_layout.insertWidget(self.list_layout.count() - 1, card)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()