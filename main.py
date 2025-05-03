from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
class Home(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/userpage.ui", self)
        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_dish = self.findChild(QPushButton, "btn_nav_dish")
        self.btn_nav_home.clicked.connect(lambda : self.navMainScreen(0))
        self.btn_nav_dish.clicked.connect(lambda : self.navMainScreen(1))
	  
    def navMainScreen(self, index):
        self.main_widget.setCurrentIndex(index)
