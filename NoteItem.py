from PyQt6.QtWidgets import QWidget, QTextEdit, QLabel, QPushButton, QSizePolicy
from PyQt6 import uic

class NoteItem(QWidget):
    def __init__(self, note_text, note_date, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/Notes_item.ui", self)

        self.text_note: QTextEdit = self.findChild(QTextEdit, "text_note")
        self.label_date: QLabel = self.findChild(QLabel, "label_date")
        self.btn_edit: QPushButton = self.findChild(QPushButton, "btn_edit")
        self.btn_delete: QPushButton = self.findChild(QPushButton, "btn_delete")

        self.text_note.setText(note_text)
        self.label_date.setText(note_date.toString("dd/MM/yyyy"))
        self.text_note.setReadOnly(True)
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.text_note.setMinimumHeight(60)
        self.text_note.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_edit.clicked.connect(self.edit_note)
        self.btn_delete.clicked.connect(self.delete_note)
        self.setMinimumSize(100, 100)

    def edit_note(self):
        if self.text_note.isReadOnly():
            self.text_note.setReadOnly(False)
            self.btn_edit.setText("Save")
        else:
            self.text_note.setReadOnly(True)
            self.btn_edit.setText("Edit")

    def delete_note(self):
        self.setParent(None)
        self.deleteLater()