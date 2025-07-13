from PyQt6.QtWidgets import QDialog, QTextEdit, QDateTimeEdit, QDialogButtonBox, QSizePolicy
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
        self.setMinimumSize(300, 200)
        self.adjustSize()

    def to_widget(self):
        note_text = self.noteEdit.toPlainText().strip()
        note_date = self.dateTimeEdit.date()
        if not note_text:
            return None
        note_widget = NoteItem(note_text, note_date)
        note_widget.setMinimumHeight(100)
        note_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        return note_widget
