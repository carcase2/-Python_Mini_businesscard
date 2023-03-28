import sys
import cv2
import re
import pytesseract
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtGui import QImage, QPixmap

# Ensure you have the correct Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_business_card(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
       print("Error: Could not load the image. Please check the file path.")
       return ""

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Extract text using OCR
    text_kor = pytesseract.image_to_string(threshold, lang='kor')
    text_eng = pytesseract.image_to_string(threshold)

    return text_kor,text_eng

class BusinessCardReader(QWidget):
    def __init__(self):
        super().__init__()

        self.label_kor = QLabel()
        self.label_kor.setWordWrap(True)

        self.label_eng = QLabel()
        self.label_eng.setWordWrap(True)

        self.button = QPushButton('Open Image')
        self.button.clicked.connect(self.load_image)

        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        
        layout.addWidget(self.button)
        
        layout1.addWidget(self.label_kor)
        layout1.addWidget(self.label_eng)

        layout.addLayout(layout1)

        self.setLayout(layout)
        self.setWindowTitle('Business Card Reader')

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)", options=options)
        
        if image_path:
            text_kor,text_eng = read_business_card(image_path)
            self.label_kor.setText(text_kor)
            self.label_eng.setText(text_eng)
        
        pattern = r'\b010[-\s]?\d{3,4}[-\s]?\d{4}\b'
        result_1 = re.search(pattern, text_kor)
        result_2 = re.search(pattern, text_kor)        
        print(result_1.group())
        print(result_2.group())
        print(text_kor)

def main():
    app = QApplication(sys.argv)
    window = BusinessCardReader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
