# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout, QDialogButtonBox,
    QLineEdit, QTextEdit, QComboBox, QLabel, QFrame
)
from PySide6.QtCore import Qt


def setup_dialog_ui(dialog):

    layout = QVBoxLayout(dialog)
    layout.setSpacing(18)
    layout.setContentsMargins(28, 24, 28, 24)

    header = QLabel(dialog.windowTitle())
    header.setObjectName("dialog_header")
    header.setStyleSheet(
        "font-size: 16px; font-weight: 700; color: #c7d2fe; "
        "letter-spacing: 0.3px; margin-bottom: 4px;"
    )
    layout.addWidget(header)

    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setStyleSheet("border: none; border-top: 1px solid #1e2437; margin-bottom: 4px;")
    layout.addWidget(separator)

    form = QFormLayout()
    form.setSpacing(14)
    form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
    form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

    dialog.title_input = QLineEdit()
    dialog.title_input.setPlaceholderText("Masukkan judul post...")
    dialog.title_input.setMinimumHeight(38)

    dialog.author_input = QLineEdit()
    dialog.author_input.setPlaceholderText("Nama penulis...")
    dialog.author_input.setMinimumHeight(38)

    dialog.slug_input = QLineEdit()
    dialog.slug_input.setPlaceholderText("url-friendly-identifier (harus unik)")
    dialog.slug_input.setMinimumHeight(38)

    dialog.status_input = QComboBox()
    dialog.status_input.addItems(["published", "draft"])
    dialog.status_input.setMinimumHeight(38)

    dialog.body_input = QTextEdit()
    dialog.body_input.setPlaceholderText("Tulis isi konten di sini...")
    dialog.body_input.setMinimumHeight(130)

    form.addRow("Title :", dialog.title_input)
    form.addRow("Author :", dialog.author_input)
    form.addRow("Slug :", dialog.slug_input)
    form.addRow("Status :", dialog.status_input)
    form.addRow("Body :", dialog.body_input)

    layout.addLayout(form)

    sep2 = QFrame()
    sep2.setFrameShape(QFrame.HLine)
    sep2.setStyleSheet("border: none; border-top: 1px solid #1e2437; margin-top: 4px;")
    layout.addWidget(sep2)

    dialog.buttons = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    )
    dialog.buttons.accepted.connect(dialog.accept)
    dialog.buttons.rejected.connect(dialog.reject)
    layout.addWidget(dialog.buttons)