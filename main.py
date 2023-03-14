import sys
from PySide6.QtWidgets import QApplication,QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)


if __name__ == "__main__":
    app = QApplication()
    
    widget = MyWidget()

    widget.show()

    sys.exit(app.exec())