
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal
import threading
from PyQt6.QtWidgets import QHBoxLayout

class FileSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QFinder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.list_widget = QListWidget() 
        self.layout.addWidget(self.list_widget)

        self.search_files()

        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.open_location_menu)

    def search_files(self):
        file_extensions = ['.docx', '.pptx', '.xlsx', '.pdf']
        search_path = "C:/Users/<change_here>/"

        def search():
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        file_path = os.path.join(root, file)
                        file_name = os.path.basename(file_path)
                        self.display_file(file_name, file_path)

        search_thread = threading.Thread(target=search)
        search_thread.start()

    def display_file(self, file_name, file_path):
        item = QListWidgetItem(self.list_widget)
        item.setText(f"Name: {file_name}\nLocation of File: {file_path}\n")
        item.setToolTip(file_path)

    def open_file(self, item):
        file_path = item.toolTip()
        os.startfile(file_path)

    def open_location_menu(self, position):
        menu = QMenu(self.list_widget)
        open_location_action = menu.addAction("Open Location")
        open_file_action = menu.addAction("Open File")
        action = menu.exec(self.list_widget.mapToGlobal(position))
        if action == open_location_action:
            item = self.list_widget.itemAt(position)
            if item is not None:
                file_path = item.toolTip()
                file_dir = os.path.dirname(file_path)
                os.startfile(file_dir)
        elif action == open_file_action:
            item = self.list_widget.itemAt(position)
            if item is not None:
                self.open_file(item)
    
    

    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSearchApp()
    window.show()

    sys.exit(app.exec())
