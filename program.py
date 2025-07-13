from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
from database import *
from weather_api import *
from NoteDialog import NoteDialog

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
        self.msg = MessageBox()

        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_account = self.findChild(QPushButton, "btn_nav_account")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_account.clicked.connect(lambda : self.navMainScreen(1))
        self.btn_nav_home.clicked.connect(lambda : self.navMainScreen(0))

        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        self.btn_avatar.clicked.connect(self.update_avatar)

        self.btn_edit = self.findChild(QPushButton, "btn_edit")
        self.btn_edit.clicked.connect(self.update_account_info)

        self.btn_logout = self.findChild(QPushButton, "btn_logout")
        self.btn_logout.clicked.connect(self.show_login)
        self.btn_calendar = self.findChild(QPushButton, "btn_calendar")
        self.btn_calendar.clicked.connect(lambda : self.navMainScreen(2))

        self.txt_city_search= self.findChild(QLineEdit, "txt_city_search")
        self.txt_city_search.returnPressed.connect(self.search_city)
        self.txt_city_search.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        self.loadAccountInfo()
        self.current_city = "Ho Chi Minh"
        self.setup_weather_widget()
        self.load_today_weather(self.current_city)

        self.btn_add_note = self.findChild(QPushButton, "btn_add_note")
        self.calendarWidget = self.findChild(QCalendarWidget, "calendarWidget")
        self.noteListWidget = self.findChild(QListWidget, "noteListWidget")
        self.user_note_days = self.findChild(QWidget, "user_note_days")
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")  
        self.noteLayout = self.user_note_days.layout()
        self.noteLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.btn_add_note.clicked.connect(self.open_note_dialog)

    def open_note_dialog(self):
        dialog = NoteDialog(self)
        dialog.dateTimeEdit.setDate(self.calendarWidget.selectedDate())

        if dialog.exec() == QDialog.DialogCode.Accepted:
            note_widget = dialog.to_widget()
            if note_widget:
                note_widget.setMinimumHeight(291)
                self.noteLayout.addWidget(note_widget)
                self.scrollArea.ensureWidgetVisible(note_widget)
            
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
        self.txt_gender.setCurrentIndex(self.txt_gender.findText(self.user.get("gender", "")))
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_birthday.setDate(QDate.fromString(self.user.get("birthday", ""), "d/M/yyyy"))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self, "Select image", "", "Images Files(*.png *.jpg *.jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.user_id, file)

    def update_account_info(self):
        msg = MessageBox()
        name = self.txt_name.text().strip()
        gender_widget = self.findChild(QComboBox, "txt_gender")
        birthday_widget = self.findChild(QDateEdit, "txt_birthday")
        birthday = birthday_widget.date().toString("d/M/yyyy")

        if gender_widget:
            gender = gender_widget.currentText()
            
        if name == "":
            msg.error_box("Họ tên không được để trống")
            self.txt_name.setFocus()
            return

        update_user(self.user_id, name, gender, birthday)  
        self.user = get_user_by_id(self.user_id)
        self.loadAccountInfo()
        msg.success_box("Cập nhật thông tin thành công")

    def search_city(self):
        city = self.txt_city_search.text().strip()
        if city:
            self.current_city = city 
            self.load_today_weather(city)
            self.setup_weather_widget()
        else:
            self.msg.error_box("Vui lòng nhập tên thành phố!")
        
    def setup_weather_widget(self):
        data_forecast = get_weather_forecast_by_name(self.current_city)
        if data_forecast["cod"] != "200":
            self.msg.error_box(data_forecast["message"])
            return False
        
        days = []
        used_dates = set()
        for item in data_forecast['list']:
            day = item['dt_txt'].split(" ")[0]
            if day not in used_dates:
                days.append(item)
                used_dates.add(day)
            if len(days) == 5:
                break

        for i, item in enumerate(days):
            img_path = f"weather_icons/{item['weather'][0]['icon']}.png"
            day = item['dt_txt'].split(" ")[0]
            description = item['weather'][0]['description']
            temp_max = item['main']['temp_max']
            temp_min = item['main']['temp_min']
            temp = item['main']['temp']
            information = f"{description.capitalize()}. High: {temp_max}°C\nLow: {temp_min}°C"

            img_weather_forecast = self.findChild(QLabel, f"img_weather_forecast_{i}")
            weather_forecast_day = self.findChild(QLabel, f"txt_weather_forecast_day_{i}")
            weather_forecast_information = self.findChild(QLabel, f"txt_weather_forecast_information_{i}")
            weather_forecast_temp = self.findChild(QLabel, f"txt_weather_forecast_temp_{i}")

            if img_weather_forecast:
                img_weather_forecast.setPixmap(QPixmap(img_path))
            if weather_forecast_day:
                weather_forecast_day.setText(day)
            if weather_forecast_information:
                weather_forecast_information.setText(information)
            if weather_forecast_temp:
                weather_forecast_temp.setText(f"{temp}°C")

    def load_today_weather(self, name):
        data = get_weather_by_name(name)
        if data["cod"] != 200:
            self.msg.error_box(data["message"])
            return False
        
        img_path = f"weather_icons/{data['weather'][0]['icon']}.png"
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather = data['weather'][0]['description']
        city = data['name']
        country = data['sys']['country']
        feel_like = data['main']['feels_like']
        high_temp = data['main']['temp_max']
        low_temp = data['main']['temp_min']
        visibility = data['visibility'] / 1000
        self.img_weather = self.findChild(QLabel, "img_weather")
        self.img_weather.setPixmap(QPixmap(img_path))
        self.txt_temp = self.findChild(QLabel, "txt_temp")
        self.txt_temp.setText(f"{temp}°C")
        self.txt_humidity = self.findChild(QLabel, "txt_humidity")
        self.txt_humidity.setText(f"Humidity: \n{humidity}%")
        self.txt_wind_speed = self.findChild(QLabel, "txt_wind_speed")
        self.txt_wind_speed.setText(f"Wind Speed:\n{wind_speed} m/s")
        self.txt_weather = self.findChild(QLabel, "txt_weather")
        self.txt_weather.setText(f"{weather.capitalize()}")
        self.txt_feel_like = self.findChild(QLabel, "txt_feel_like")
        self.txt_feel_like.setText(f"Feels like: \n{feel_like}°C")
        self.txt_city_name_main = self.findChild(QLabel, "txt_city_name_main")
        self.txt_city_name_main.setText(f"{city}, \n{country}")
        self.txt_city_name = self.findChild(QLabel, "txt_city_name")
        self.txt_city_name.setText(f"{city}, {country}")
        self.txt_high_temp = self.findChild(QLabel, "txt_high_temp")
        self.txt_high_temp.setText(f"High: \n{high_temp}°C")
        self.txt_low_temp = self.findChild(QLabel, "txt_low_temp")
        self.txt_low_temp.setText(f"Low: \n{low_temp}°C")
        self.txt_visibility = self.findChild(QLabel, "txt_visibility")
        self.txt_visibility.setText(f"Visibility: \n{visibility} km")

if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    login=Home(1)
    login.show()
    app.exec()  