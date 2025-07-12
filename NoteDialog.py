from PyQt6.QtWidgets import QDialog, QTextEdit, QDateTimeEdit, QDialogButtonBox, QWidget, QVBoxLayout, QLabel
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

        self.setWindowTitle("Thêm ghi chú")
        self.setMinimumSize(100, 100)
        self.adjustSize()

    def to_widget(self):
        note_text = self.noteEdit.toPlainText()
        note_date = self.dateTimeEdit.date()
        return NoteItem(note_text, note_date)
