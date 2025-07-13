from PyQt6.QtWidgets import QDialog, QTextEdit, QDialogButtonBox, QDateTimeEdit
from PyQt6 import uic
from NoteItem import NoteItem

class NoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/Notes_dialog.ui", self)

        self.noteEdit: QTextEdit = self.findChild(QTextEdit, "textEdit")
        self.dateTimeEdit: QDateTimeEdit = self.findChild(QDateTimeEdit, "dateTimeEdit")
        self.buttonBox: QDialogButtonBox = self.findChild(QDialogButtonBox, "buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle("   ")

    def get_note_data(self):
        text = self.noteEdit.toPlainText().strip()
        date = self.dateTimeEdit.dateTime() 
        return text, date