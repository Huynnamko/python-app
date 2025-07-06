from PyQt6.QtWidgets import QDialog, QTextEdit, QDialogButtonBox, QVBoxLayout

class NoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")
        self.setFixedSize(300, 200)

        self.text_edit = QTextEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_note(self):
        return self.text_edit.toPlainText().strip()