# Starts the app
# Opens the main window and runs it

import sys
from PyQt6.QtWidgets import QApplication
from main_window import Win

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Win()
    sys.exit(app.exec())