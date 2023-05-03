import sys
import cv2
import re
import pytesseract
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QFrame, QLineEdit, QListWidget
from PySide6.QtGui import QImage, QPixmap
from pymongo import MongoClient
from PySide6.QtCore import Qt


# Ensure you have the correct Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


people = {
    'names': [],
    'ages': [],
    'phone': [],
}

def connect_to_db():
    # Connect to local MongoDB instance
    client = MongoClient('mongodb+srv://carcase2:1850017@cluster0.9gddo.mongodb.net/?retryWrites=true&w=majority')
    
    # Create or connect to the 'business_cards' database
    db = client['business_cards']
    
    # Create or connect to the 'contacts' collection
    contacts_collection = db['contacts']
    
    print("ok mongodb")
    
    return contacts_collection

def save_to_db(collection, email, phone, fax):
    # Create a dictionary to store the contact data
    contact_data = {
        'email': email,
        'phone': phone,
        'fax' : fax
    }
    
    # Insert the contact data into the MongoDB collection
    result = collection.insert_one(contact_data)
    
    # Print the result
    print(f"Data saved with ID: {result.inserted_id}")

def read_business_card(image_path):
    global image
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
        
    # text_eng = text_eng.replace("!", "1")
    
    # print(text_eng)
    # print(text_kor)

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
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(800, 600)  # 창 크기를 800x600으로 설정
        self.setWindowTitle("Business Card Reader")
        self.show()    
        
        self.label_Email_text = QLabel()
        # self.label_Email.setWordWrap(True)
        self.label_Email_text.setFixedSize(100, 50)
        
        self.label_Email = QLabel()
        self.label_Email.setWordWrap(True)

        self.label_Phone_1 = QLabel()
        self.label_Phone_1_text = QLabel()
        self.label_Phone_1_text.setFixedSize(100, 50)
                  
        self.label_Phone_1.setWordWrap(True)

        self.label_Fax = QLabel()
        self.label_Fax_text = QLabel()
        self.label_Fax_text.setFixedSize(100, 50)

        self.label_Fax.setWordWrap(True)

        self.label_kor = QLabel()
        self.label_kor.setWordWrap(True)

        self.label_eng = QLabel()
        self.label_eng.setWordWrap(True)

        self.button = QPushButton('Open Image')
        self.button.setFixedSize(400, 50)

        self.button.clicked.connect(self.load_image)

        layout_main = QHBoxLayout()
        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout_right = QVBoxLayout()

        layout_email = QHBoxLayout()
        layout_Phone1 = QHBoxLayout()
        layout_Fax = QHBoxLayout()
        
        label_right = QLabel("This is an example text for the right layout.")
        layout_right.addWidget(label_right)
        
        
        layout_email.addWidget(self.label_Email_text)
        layout_email.addWidget(self.label_Email)
        
        layout_Phone1.addWidget(self.label_Phone_1_text)
        layout_Phone1.addWidget(self.label_Phone_1)
        
        layout_Fax.addWidget(self.label_Fax_text)
        layout_Fax.addWidget(self.label_Fax)
       
        layout.addWidget(self.button)        
        layout1.addWidget(self.label_kor)
        layout1.addWidget(self.label_eng)
        
        layout1.addLayout(layout_email)
        layout1.addLayout(layout_Phone1)
        layout1.addLayout(layout_Fax)
        
        container1 = QWidget()
        container1.setLayout(layout1)
        container1.setFixedSize(400, 500)
        
        # 검색 창 및 목록 창 위젯 생성
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.list_widget = QListWidget()
    
        # 검색 창 및 목록 창 위젯을 layout_right에 추가
        layout_right.addWidget(self.search_bar)
        layout_right.addWidget(self.list_widget)
        
        self.label_Email_text.setText("E-mail")
        self.label_Phone_1_text.setText("Phone")      
        self.label_Fax_text.setText("FAX")
        
        layout.addWidget(container1)
        layout.addLayout(layout1)
        
        
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        layout_main.addLayout(layout)
        layout_main.addWidget(separator)
        layout_main.addLayout(layout_right)
        
        self.setLayout(layout_main)


    def load_image(self):
        desired_width = 400
        desired_height = 300
        
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)", options=options)
        contacts_collection = connect_to_db()
        if image_path:
            
            text_kor,text_eng = read_business_card(image_path)
            text_kor_without_spaces = "".join(text_kor.split())
            text_eng_without_spaces = "".join(text_eng.split())
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_kor.setFixedSize(desired_width, desired_height)
            self.label_kor.setPixmap(scaled_pixmap)
            # self.label_kor.setPixmap(pixmap)
            # self.label_eng.setText(text_eng)
            # print(type(text_eng))
            print(text_kor_without_spaces)
            # fax 글짜 위치 찾기 위해서
            location = text_eng.find("FAX")
            # print(location)
            # print(text_eng[112])
            # print(text_eng[113])
            # print(text_eng[114])
            # print(location + len("FAX"))
            fax_string = text_eng[location + 3:location + 18]
            pattern = r'\b\d{2,3}[-\s]?\d{3,4}[-\s]?\d{4}\b'
            result_fax = re.search(pattern, fax_string) 
            if result_fax is not None:
                self.label_Fax.setText(result_fax.group())
            else:
                print(fax_string)
                
            # print(result_fax.group())
            
            # self.label_Fax.setText(result_fax.group())
            
            pattern = r'\b010[-\s]?\d{3,4}[-\s]?\d{4}\b'
            result_1 = re.search(pattern, text_kor)
            result_phone = re.search(pattern, text_eng)        

            location = text_kor_without_spaces.find("김")
            print('location = ', location)
            print(text_kor_without_spaces[10])
            print(text_kor_without_spaces[11])
            print(text_kor_without_spaces[12])
                                                
            # if result_1 is not None and result_phone is not None:
            #     print("휴대폰",result_1.group())
            #     print("휴대폰",result_phone.group())
            #     self.label_Phone_1.setText(result_phone.group())
            # else:            
            #     print("No match found.")
                
            email = extract_email(text_eng)
            print(text_eng)
            
            
            
            if email:
                print(f"Email: {email}")
                self.label_Email.setText(email)
                
            else:
                email="No email found."
                self.label_Email.setText(email)
                # print("No email found.")    
        
            if result_fax is not None : 
                fax_group = result_fax.group()
                # save_to_db(contacts_collection, email, result_phone.group(), result_fax.group())     
            else:
                print("No fax found.")
                fax_group = "No fax found."
                # save_to_db(contacts_collection, email, result_phone.group(), fax_group)     
                
            if result_phone is not None : 
                # save_to_db(contacts_collection, email, result_phone.group(), result_fax.group())     
                phone_group = result_phone.group()
            else:
                print("No phone found.")
                phone_group = "No phone found."
                # save_to_db(contacts_collection, email, result_phone.group(), fax_group)   
            
            self.label_Fax.setText(fax_group)          
            self.label_Phone_1.setText(phone_group)
            
        save_to_db(contacts_collection, email, phone_group, fax_group)         
        # Append values for the second person
        people['names'].append('Jane Smith')
        people['ages'].append(28)
        people['phone'].append(phone_group)

        print(people['phone'])
                
def main():
    app = QApplication(sys.argv)
    window = BusinessCardReader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
