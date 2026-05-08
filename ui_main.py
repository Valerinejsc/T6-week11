# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget,
    QScrollArea, QSplitter, QHeaderView, QFrame
)

def setup_main_ui(window):
    central = QWidget()
    window.setCentralWidget(central)

    root = QVBoxLayout(central)
    root.setSpacing(0)
    root.setContentsMargins(0, 0, 0, 0)

    top_bar = QFrame()
    top_bar.setObjectName("top_bar")
    top_bar.setStyleSheet(
        "#top_bar {"
        "  background-color: #0b0e18;"
        "  border-bottom: 1px solid #1e2437;"
        "  min-height: 55px;"
        "  max-height: 55px;"
        "}"
    )
    top_layout = QHBoxLayout(top_bar)
    top_layout.setContentsMargins(10, 0, 10, 0)
    top_layout.setSpacing(12)

    app_title = QLabel("📋 Post Manager")
    app_title.setStyleSheet(
        "background: transparent; font-size: 15px; font-weight: 700; color: #818cf8; letter-spacing: 0.7px;"
    )
    top_layout.addWidget(app_title)
    top_layout.addStretch()

    window.status_label = QLabel("Ready")
    window.status_label.setObjectName("status_label")
    top_layout.addWidget(window.status_label)

    root.addWidget(top_bar)

    toolbar = QFrame()
    toolbar.setObjectName("toolbar")
    toolbar.setStyleSheet(
        "#toolbar {"
        "  background-color: #0d1120;"
        "  border-bottom: 1px solid #1a1f30;"
        "  min-height: 52px;"
        "  max-height: 52px;"
        "}"
    )
    toolbar_layout = QHBoxLayout(toolbar)
    toolbar_layout.setContentsMargins(20, 0, 20, 0)
    toolbar_layout.setSpacing(8)

    window.btn_refresh = QPushButton("⟳  Refresh")
    window.btn_refresh.setObjectName("btn_refresh")

    window.btn_tambah = QPushButton("＋  Tambah Post")
    window.btn_tambah.setObjectName("btn_tambah")

    window.btn_edit = QPushButton("✎  Edit Post")
    window.btn_edit.setObjectName("btn_edit")
    window.btn_edit.setEnabled(False)

    window.btn_hapus = QPushButton("✕  Hapus Post")
    window.btn_hapus.setObjectName("btn_hapus")
    window.btn_hapus.setEnabled(False)

    for btn in [window.btn_refresh, window.btn_tambah,
                window.btn_edit, window.btn_hapus]:
        btn.setMinimumHeight(34)
        toolbar_layout.addWidget(btn)

    toolbar_layout.addStretch()
    root.addWidget(toolbar)

    content = QFrame()
    content.setStyleSheet("background-color: #0f1117;")
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(16, 16, 16, 16)
    content_layout.setSpacing(0)

    splitter = QSplitter(Qt.Horizontal)
    splitter.setHandleWidth(4)

    table_frame = QFrame()
    table_frame.setStyleSheet(
        "QFrame { background: transparent; }"
    )
    table_frame_layout = QVBoxLayout(table_frame)
    table_frame_layout.setContentsMargins(0, 0, 8, 0)
    table_frame_layout.setSpacing(0)

    window.table = QTableWidget()
    window.table.setColumnCount(4)
    window.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'Status'])
    window.table.setSelectionBehavior(QTableWidget.SelectRows)
    window.table.setEditTriggers(QTableWidget.NoEditTriggers)
    window.table.setAlternatingRowColors(True)
    window.table.verticalHeader().setVisible(False)
    window.table.setShowGrid(False)

    header = window.table.horizontalHeader()
    header.setSectionResizeMode(1, QHeaderView.Stretch)
    window.table.setColumnWidth(0, 50)
    window.table.setColumnWidth(2, 130)
    window.table.setColumnWidth(3, 100)

    window.table.verticalHeader().setDefaultSectionSize(40)

    table_frame_layout.addWidget(window.table)
    splitter.addWidget(table_frame)

    detail_frame = QFrame()
    detail_frame.setStyleSheet("QFrame { background: transparent; }")
    detail_frame_layout = QVBoxLayout(detail_frame)
    detail_frame_layout.setContentsMargins(8, 0, 0, 0)
    detail_frame_layout.setSpacing(8)

    detail_header = QLabel("DETAIL POST")
    detail_header.setStyleSheet(
        "font-size: 11px; font-weight: 600; color: #4f5a80; "
        "letter-spacing: 1px; padding: 0 2px 6px 2px;"
        "border-bottom: 1px solid #1e2437;"
    )
    detail_frame_layout.addWidget(detail_header)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.NoFrame)
    scroll.setStyleSheet("QScrollArea { background: #12151f; border-radius: 10px; }")

    window.detail_inner = QWidget()
    window.detail_inner.setStyleSheet("background: #12151f; border-radius: 10px;")
    window.detail_inner_layout = QVBoxLayout(window.detail_inner)
    window.detail_inner_layout.setContentsMargins(16, 16, 16, 16)
    window.detail_inner_layout.setSpacing(10)
    window.detail_inner_layout.setAlignment(Qt.AlignTop)

    window.detail_placeholder = QLabel("Klik baris pada tabel untuk melihat detail post...")
    window.detail_placeholder.setAlignment(Qt.AlignCenter)
    window.detail_placeholder.setStyleSheet(
        "color: #2d3450; font-size: 13px; padding: 40px;"
    )
    window.detail_inner_layout.addWidget(window.detail_placeholder)

    scroll.setWidget(window.detail_inner)
    detail_frame_layout.addWidget(scroll)

    splitter.addWidget(detail_frame)
    splitter.setSizes([600, 380])

    content_layout.addWidget(splitter)
    root.addWidget(content)