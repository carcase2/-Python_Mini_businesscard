import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QLabel,QWidget,QVBoxLayout,QHBoxLayout,QFrame,QSizePolicy
from PySide6.QtGui import QPixmap
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'


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
        self.setFixedSize(1000, 600)

        card_image = Image.open('business_card.jpg')
        text = pytesseract.image_to_string(card_image)
        
        # 윈도우 title 명 지정
        # setFixedSize는 QWidget에 들어가 있음
        # class QMainxWindow(PySide6.QtWidgets.QWidget):
        # QmainWindos는 QWidget이라는 부모를 가지고 그 부모에 setWindowTitle를 이용하는거
        self.setWindowTitle("명함인식 by KKD")

        # create a central widget and set it as the main window's main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
         # create a button for opening image file
        self.button = QPushButton('Open Image', self)
        self.button.clicked.connect(self.open_image)

        # create a label for displaying image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 500)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        # add a line
        line1 = QFrame(self)
        line1.setFrameShape(QFrame.VLine)
        layout.addWidget(line1)
     
        # line2 = QFrame(self)
        # line2.setFrameShape(QFrame.VLine)
        # line2.setFrameShadow(QFrame.Raised)
        # layout.addWidget(line2)
        main_layout2 = QVBoxLayout()
        
        self.button1 = QPushButton('명함인식', self)
        self.button2 = QPushButton('명함인식2', self)
        self.text_label1 = QLabel(self)
        self.text_label1.setFixedSize(200, 50)
        self.text_label1.setStyleSheet("border: 1px solid red;")
        
        self.text_label2 = QLabel(self)
        self.text_label3 = QLabel(self)
        self.text_label4 = QLabel(self)
        
        main_layout2.addWidget(self.button1)
        main_layout2.addWidget(self.button2)
        main_layout2.addWidget(self.text_label1)
        main_layout2.addWidget(self.text_label2)
        main_layout2.addWidget(self.text_label3)
        main_layout2.addWidget(self.text_label4)
        # self.text_label1.setText(text)
        self.text_label2.setText("2")
        self.text_label3.setText("3")
        self.text_label4.setText("4")
        
        
        # layout.addWidget(self.button1)
        layout.addLayout(main_layout2)
        # add button and label to the main window
        # self.setCentralWidget(self.image_label)
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
