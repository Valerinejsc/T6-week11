# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

from PySide6.QtWidgets import QDialog
from ui_dialog import setup_dialog_ui


class PostDialog(QDialog):
    def __init__(self, parent=None, post=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Post" if post else "Tambah Post Baru")
        self.setMinimumWidth(480)

        setup_dialog_ui(self)

        if post:
            self.title_input.setText(post.get('title', ''))
            self.author_input.setText(post.get('author', ''))
            self.slug_input.setText(post.get('slug', ''))
            self.body_input.setPlainText(post.get('body', ''))

            index = self.status_input.findText(post.get('status', 'draft'))
            if index >= 0:
                self.status_input.setCurrentIndex(index)

    def get_data(self):
        return {
            'title': self.title_input.text().strip(),
            'author': self.author_input.text().strip(),
            'slug': self.slug_input.text().strip(),
            'status': self.status_input.currentText(),
            'body': self.body_input.toPlainText().strip()
        }