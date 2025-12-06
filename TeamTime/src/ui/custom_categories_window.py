from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt

class CustomCategoriesWindow(QDialog):
    def __init__(self, categorizer, parent=None):
        super().__init__(parent)
        self.categorizer = categorizer
        self.setWindowTitle("Custom Categories")
        self.setGeometry(200, 200, 700, 600)
        self.setStyleSheet("background-color: #0a0a0a; color: #ffffff;")

        self.init_ui()
        self.load_custom_categories()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("📝 Your Custom Categories")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
        """)

        # Productive list
        productive_label = QLabel("✅ Productive Apps")
        productive_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            background-color: #27ae60;
            padding: 8px;
            border-radius: 8px;
        """)

        self.productive_list = QListWidget()
        self.productive_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
        """)

        # Distracting list
        distracting_label = QLabel("❌ Distracting Apps")
        distracting_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            background-color: #e74c3c;
            padding: 8px;
            border-radius: 8px;
        """)

        self.distracting_list = QListWidget()
        self.distracting_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #e74c3c;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
        """)

        # Neutral list
        neutral_label = QLabel("➖ Neutral Apps")
        neutral_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            background-color: #95a5a6;
            padding: 8px;
            border-radius: 8px;
        """)

        self.neutral_list = QListWidget()
        self.neutral_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #95a5a6;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
        """)

        # Buttons
        button_layout = QHBoxLayout()

        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)

        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        # Add all to layout
        layout.addWidget(title_label)
        layout.addWidget(productive_label)
        layout.addWidget(self.productive_list)
        layout.addWidget(distracting_label)
        layout.addWidget(self.distracting_list)
        layout.addWidget(neutral_label)
        layout.addWidget(self.neutral_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_custom_categories(self):
        # Load from the categorizer
        categories = self.categorizer.categories

        # Get manually changed apps
        manually_changed = categories.get("manually_changed", [])

        # Add only manually changed apps to the appropriate lists
        for app in manually_changed:
            if app in categories.get("productive", []):
                self.productive_list.addItem(app)
            elif app in categories.get("distracting", []):
                self.distracting_list.addItem(app)
            elif app in categories.get("neutral", []):
                self.neutral_list.addItem(app)

    def delete_selected(self):
        # Find which list has a selected item
        selected_list = None
        category = None

        if self.productive_list.currentItem():
            selected_list = self.productive_list
            category = "productive"
        elif self.distracting_list.currentItem():
            selected_list = self.distracting_list
            category = "distracting"
        elif self.neutral_list.currentItem():
            selected_list = self.neutral_list
            category = "neutral"

        if not selected_list or not category:
            QMessageBox.warning(self, "No Selection", "Please select an app to delete.")
            return

        # Get the selected item
        current_item = selected_list.currentItem()
        app_name = current_item.text()

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to remove '{app_name}' from {category}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Remove from categorizer
            self.categorizer.remove_rule(category, app_name)
            # Also remove from manually_changed list
            if "manually_changed" in self.categorizer.categories:
                if app_name in self.categorizer.categories["manually_changed"]:
                    self.categorizer.categories["manually_changed"].remove(app_name)
                    self.categorizer.save_categories()
            # Remove from list
            selected_list.takeItem(selected_list.row(current_item))
            QMessageBox.information(self, "Deleted", f"'{app_name}' has been removed.")
