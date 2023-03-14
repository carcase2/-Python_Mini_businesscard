import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QLabel
from PySide6.QtGui import QPixmap


class MyWidget(QMainWindow):
    # 이 class가 선언되면 실행된다.
    # 클래스의 인스턴스를 초기화하는 데 사용됩니다. 이 메소드는 클래스의 새 인스턴스가 생성될 때 자동으로 호출되며, 인스턴스의 초기 상태를 설정하는 데 사용할 수 있습니다.
    def __init__(self):
        # 부모 클래스 init
        # 부모님은 super man임
        super().__init__()
        # 창 사이즈 지정
        # 위 super가 없으면 setFixedSize 함수 사용 안됨
        # setFixedSize는 QWidget에 들어가 있음
        # class QMainxWindow(PySide6.QtWidgets.QWidget):
        # QmainWindos는 QWidget이라는 부모를 가지고 그 부모에 setFixedSize를 이용하는거
        # 창 사이즈 지정
        self.setFixedSize(600, 400)

        # 윈도우 title 명 지정
        # setFixedSize는 QWidget에 들어가 있음
        # class QMainxWindow(PySide6.QtWidgets.QWidget):
        # QmainWindos는 QWidget이라는 부모를 가지고 그 부모에 setWindowTitle를 이용하는거
        self.setWindowTitle("명함인식 by KKD")

         # create a button for opening image file
        self.button = QPushButton('Open Image', self)
        self.button.clicked.connect(self.open_image)

        # create a label for displaying image
        self.image_label = QLabel(self)
        # self.image_label.setFixedSize(400, 200)
        self.image_label.setAlignment(Qt.AlignCenter)

        # add button and label to the main window
        self.setCentralWidget(self.image_label)
        self.toolbar = self.addToolBar('Open')
        self.toolbar.addWidget(self.button)

    def open_image(self):
        # open a file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')

        if file_name:
            # display the selected image in the label
            pixmap = QPixmap(file_name)
            # set the pixmap as the label's background and scale it to fit the label
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)   

        # enable scaled contents so that the pixmap will be scaled automatically when the label is resized
            # self.image_label.setScaledContents(True)
            

            
            
            
if __name__ == "__main__":

    app = QApplication()

    widget = MyWidget()

    widget.show()

    sys.exit(app.exec())
