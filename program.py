from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
from database import *

class MessageBox():
    def success_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
    
    def error_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui",self)

        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))

    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye_open-removebg-preview.png"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye_close-removebg-preview.png"))

    def login(self):
        msg = MessageBox()
        email = self.email.text().strip()
        password = self.password.text().strip()

        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return

        user = get_user_by_email_and_password(email, password)
        if user is not None:
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
            return

        msg.error_box("Email hoặc mật khẩu không đúng")

    def show_home(self, user_id):
        self.home = Home(user_id)
        self.home.show()
        self.close()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        
        self.name = self.findChild(QLineEdit, "txt_name")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_login.clicked.connect(self.show_login)
        self.btn_register.clicked.connect(self.register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        self.btn_eye_cp.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_eye_cp))

    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye_open-removebg-preview.png"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye_close-removebg-preview.png"))

    def register(self):
        msg = MessageBox()
        name = self.name.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if name =="":
            msg.error_box("Họ tên không được để trống")
            self.name.setFocus()
            return

        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return

        if confirm_password == "":
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return

        if password != confirm_password:
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not self.validate_email(email):
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return

        check_email = get_user_by_email(email)
        if check_email is not None:
            msg.error_box("Email đã tồn tại")
            return

        create_user(name,email,password)
        msg.success_box("Đăng ký thành công")
        self.show_login()

    def validate_email(self,s):   
        idx_at = s.find('@')
        if idx_at == -1:
            return False
        return '.' in s[idx_at+1:]

    def show_login(self):
        self.login= Login()
        self.login.show()
        self.close()

class Home(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/userpage.ui", self)

        self.user_id = user_id
        self.user=get_user_by_id(self.user_id)

        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_account = self.findChild(QPushButton, "btn_nav_account")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_account.clicked.connect(lambda : self.navMainScreen(1))
        self.btn_nav_home.clicked.connect(lambda : self.navMainScreen(0))

        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        self.btn_avatar.clicked.connect(self.upadate_avatar)

        self.btn_edit = self.findChild(QPushButton, "btn_edit")
        self.btn_edit.clicked.connect(self.update_account_info)


        self.btn_logout = self.findChild(QPushButton, "btn_logout")
        self.btn_logout.clicked.connect(self.show_login)
        self.btn_calendar = self.findChild(QPushButton, "btn_calendar")
        self.btn_calendar.clicked.connect(lambda : self.navMainScreen(2))

        self.loadAccountInfo()

    def navMainScreen(self, index):
        self.main_widget.setCurrentIndex(index)

    def show_login(self):
        self.login= Login()
        self.login.show()
        self.close()

    def loadAccountInfo(self):
        self.txt_name = self.findChild(QLineEdit,"txt_name")
        self.txt_email = self.findChild(QLineEdit,"txt_email")
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"]))
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
                                         
    def upadate_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self, "Select image", "", "Images Files(*.png *.jpg *.jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.user_id, file)

    def update_account_info(self):
        msg = MessageBox()
        name = self.txt_name.text().strip()
        gender_widget = self.findChild(QComboBox, "txt_gender")
        if gender_widget:
            gender = gender_widget.currentText()

        if name == "":
            msg.error_box("Họ tên không được để trống")
            self.txt_name.setFocus()
            return
        if gender == "":
            msg.error_box("Giới tính không được để trống")
            return

        try:
            update_user(self.user_id, name, gender)  
            self.user = get_user_by_id(self.user_id)
            self.loadAccountInfo()
            msg.success_box("Cập nhật thông tin thành công")
        except Exception as e:
            msg.error_box(f"Lỗi cập nhật: {e}")

if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    login.show()
    app.exec()  

