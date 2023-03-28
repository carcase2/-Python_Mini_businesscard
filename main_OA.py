import sys
import cv2
import pytesseract
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
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
    text = pytesseract.image_to_string(threshold)

    return text

class BusinessCardReader(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.label.setWordWrap(True)

        self.button = QPushButton('Open Image')
        self.button.clicked.connect(self.load_image)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle('Business Card Reader')

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)", options=options)
        
        if image_path:
            text = read_business_card(image_path)
            self.label.setText(text)

def main():
    app = QApplication(sys.argv)
    window = BusinessCardReader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
