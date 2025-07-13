from PyQt6.QtWidgets import QWidget, QTextEdit, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic

class NoteItem(QWidget):
    delete_requested = pyqtSignal(int)
    update_requested = pyqtSignal(int, str)
    status_changed = pyqtSignal(int, str)

    def __init__(self, note_id, note_text, note_date, status="0", parent=None):
        super().__init__(parent)
        uic.loadUi("ui/Notes_item.ui", self)

        self.note_id = note_id
        self.status = status

        self.text_note: QTextEdit = self.findChild(QTextEdit, "text_note")
        self.label_date: QLabel = self.findChild(QLabel, "label_date")
        self.btn_edit: QPushButton = self.findChild(QPushButton, "btn_edit")
        self.btn_delete: QPushButton = self.findChild(QPushButton, "btn_delete")

        self.text_note.setText(note_text)
        self.label_date.setText(note_date.toString("dd/MM/yyyy HH:mm AP"))
        self.text_note.setReadOnly(True)
        self.apply_status_font()

        self.btn_edit.clicked.connect(self.edit_note)
        self.btn_delete.clicked.connect(self.delete_note)
        self.text_note.mouseDoubleClickEvent = self.toggle_status
        self.original_text = note_text
        self.show()


    def apply_status_font(self):
        font = self.text_note.font()
        font.setStrikeOut(self.status in ["1", "done"])
        self.text_note.setFont(font)

    def toggle_status(self, event):
        self.status = "0" if self.status in ["1", "done"] else "1"
        self.apply_status_font()
        self.status_changed.emit(self.note_id, self.status)
        
    def edit_note(self):
        if self.text_note.isReadOnly():
            self.text_note.setReadOnly(False)
            self.btn_edit.setText("Save")
        else:
            self.text_note.clearFocus() 
            new_text = self.text_note.toPlainText().strip()
            self.text_note.setReadOnly(True)
            self.btn_edit.setText("Edit")

            if new_text != self.original_text:
                self.original_text = new_text
                self.update_requested.emit(self.note_id, new_text)

    def delete_note(self):
        self.delete_requested.emit(self.note_id)
