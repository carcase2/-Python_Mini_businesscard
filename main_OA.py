import sys
import cv2
import re
import pytesseract
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtGui import QImage, QPixmap

# Ensure you have the correct Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


people = {
    'names': [],
    'ages': [],
    'phone': [],
}

def read_business_card(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
       print("Error: Could not load the image. Please check the file path.")
       return ""

    # Preprocess the image
    
    # 이미지 스케일 업
    image_upscale = cv2.pyrUp(image)
    
    image_upscale2 = cv2.pyrUp(image_upscale)
    
    saved = cv2.imwrite('saved_image.png', image_upscale)
    
    # image 내용 확인 
    height,width,channels= image.shape
    print(height,width,channels)
    
    height,width,channels= image_upscale.shape
    print(height,width,channels)
    
    height,width,channels= image_upscale2.shape
    print(height,width,channels)
    
    saved = cv2.imwrite('saved_image2.png', image_upscale2)

    
    gray = cv2.cvtColor(image_upscale2, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Extract text using OCR
    text_kor = pytesseract.image_to_string(threshold, lang='kor')
    text_eng = pytesseract.image_to_string(threshold)
        
    text_eng = text_eng.replace("!", "1")
    
    # print(text_eng)
    # print(text_kor)
    email = extract_email(text_eng)
    
    if email:
        print(f"Email: {email}")
    else:
        print("No email found.")
    return text_kor,text_eng

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    result = re.search(pattern, text)
    if result:
        return result.group()
    return None

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
        layout1 = QVBoxLayout()
        
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
            text_kor_without_spaces = "".join(text_kor.split())
            text_eng_without_spaces = "".join(text_eng.split())
            self.label_kor.setText(text_kor_without_spaces)
            self.label_eng.setText(text_eng_without_spaces)
        
        pattern = r'\b010[-\s]?\d{3,4}[-\s]?\d{4}\b'
        result_1 = re.search(pattern, text_kor)
        result_2 = re.search(pattern, text_eng)        
        
        
        if result_1 is not None and result_2 is not None:
            print("휴대폰",result_1.group())
            print("휴대폰",result_2.group())
        else:            
            print("No match found.")
            
        # Append values for the second person
        people['names'].append('Jane Smith')
        people['ages'].append(28)
        people['phone'].append(result_1.group())

        print(people['phone'])
                
def main():
    app = QApplication(sys.argv)
    window = BusinessCardReader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
