# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

import sys
import os
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog,
    QLabel, QHBoxLayout, QFrame, QWidget
)

from dialogs import PostDialog
from api_worker import ApiWorker
from ui_main import setup_main_ui


def load_stylesheet(app):
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def _make_separator():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet("background-color: #1e2437; border: none; margin: 4px 0;")
    return line


def _make_comment_card(body_text):
    card = QFrame()
    card.setStyleSheet(
        "QFrame {"
        "  background-color: #161a27;"
        "  border-left: 3px solid #4f60c0;"
        "  border-radius: 4px;"
        "  padding: 2px;"
        "}"
    )
    card_layout = QHBoxLayout(card)
    card_layout.setContentsMargins(10, 8, 10, 8)

    lbl = QLabel(body_text)
    lbl.setWordWrap(True)
    lbl.setStyleSheet("font-size: 12px; color: #94a3b8; background: transparent;")
    card_layout.addWidget(lbl)
    return card


class PostViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Post Manager — REST API Desktop")
        self.setGeometry(100, 100, 1060, 660)

        self.posts_data = [] 
        self._thread = None
        self._worker = None

        setup_main_ui(self)
        self._connect_signals()

        self.fetch_posts()  


    def _connect_signals(self):
        self.btn_refresh.clicked.connect(self.fetch_posts)
        self.btn_tambah.clicked.connect(self.add_post)
        self.btn_edit.clicked.connect(self.edit_post)
        self.btn_hapus.clicked.connect(self.delete_post)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)


    def run_worker(self, action, on_success, **kwargs):
        self._thread = QThread()
        self._worker = ApiWorker(action, **kwargs)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(on_success)
        self._worker.error.connect(self.on_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(lambda: self.set_loading(False))

        self.set_loading(True)
        self._thread.start()

    def set_loading(self, is_loading):
        for btn in [self.btn_refresh, self.btn_tambah, self.btn_edit, self.btn_hapus]:
            if btn in [self.btn_edit, self.btn_hapus] and not is_loading:
                btn.setEnabled(self.table.currentRow() >= 0)
            else:
                btn.setEnabled(not is_loading)

        if is_loading:
            self.status_label.setText("⏳  Sedang memproses data...")
            self.status_label.setFixedHeight(35)
            self.status_label.setStyleSheet(
                "color: #60a5fa; font-weight: 600; font-size: 12px; "
                "background: #1a2535; border: 1px solid #2a4a7f; "
                "border-radius: 6px;"
            )

    def fetch_posts(self):
        self.run_worker("get_posts", self.on_posts_loaded)

    def on_posts_loaded(self, posts):
        self.posts_data = posts
        self.table.setRowCount(0)

        from PySide6.QtWidgets import QTableWidgetItem
        from PySide6.QtCore import Qt

        STATUS_COLOR = {
            "published": "#4ade80",
            "draft":     "#fbbf24",
        }

        for p in self.posts_data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            id_item = QTableWidgetItem(str(p['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, QTableWidgetItem(p['title']))
            self.table.setItem(row, 2, QTableWidgetItem(p['author']))

            status_item = QTableWidgetItem(p['status'])
            status_item.setTextAlignment(Qt.AlignCenter)
            color = STATUS_COLOR.get(p['status'], "#94a3b8")
            status_item.setForeground(__import__('PySide6.QtGui', fromlist=['QColor']).QColor(color))
            self.table.setItem(row, 3, status_item)

        self.status_label.setText(f"✅  {len(posts)} posts dimuat")
        self.status_label.setStyleSheet(
            "color: #4ade80; font-weight: 600; font-size: 12px; "
            "background: #1a2e26; border: 1px solid #1e5c3a; "
            "border-radius: 6px; padding: 4px 12px;"
        )


    def on_selection_changed(self):
        row = self.table.currentRow()
        if row < 0:
            self.btn_edit.setEnabled(False)
            self.btn_hapus.setEnabled(False)
            return

        self.btn_edit.setEnabled(True)
        self.btn_hapus.setEnabled(True)

        post_id = self.table.item(row, 0).text()
        self.run_worker("get_post", self.on_detail_loaded, post_id=post_id)

    def on_detail_loaded(self, post):
        self._clear_detail_panel()

        comments_list = post.get('comments', [])
        layout = self.detail_inner_layout

        lbl_title = QLabel(post['title'])
        lbl_title.setWordWrap(True)
        lbl_title.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #c7d2fe; "
            "padding-bottom: 6px;"
        )
        layout.addWidget(lbl_title)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(8)

        lbl_author = QLabel(f"✍  {post['author']}")
        lbl_author.setStyleSheet("font-size: 12px; color: #7c88b0;")

        sep1 = QLabel("|")
        sep1.setStyleSheet("color: #2d3450;")

        status_color = "#4ade80" if post['status'] == "published" else "#fbbf24"
        lbl_status = QLabel(f"● {post['status'].upper()}")
        lbl_status.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {status_color};"
        )

        sep2 = QLabel("|")
        sep2.setStyleSheet("color: #2d3450;")

        lbl_slug = QLabel(post['slug'])
        lbl_slug.setStyleSheet("font-size: 12px; color: #4f5a80;")

        for w in [lbl_author, sep1, lbl_status, sep2, lbl_slug]:
            meta_row.addWidget(w)
        meta_row.addStretch()
        layout.addLayout(meta_row)

        layout.addWidget(_make_separator())

        lbl_body = QLabel(post['body'])
        lbl_body.setWordWrap(True)
        lbl_body.setStyleSheet(
            "font-size: 13px; color: #cbd5e1; line-height: 1.7; padding: 2px 0;"
        )
        layout.addWidget(lbl_body)

        layout.addWidget(_make_separator())

        lbl_komentar_header = QLabel("KOMENTAR")
        lbl_komentar_header.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #4f5a80; letter-spacing: 1px;"
        )
        layout.addWidget(lbl_komentar_header)

        if comments_list:
            for c in comments_list:
                card = _make_comment_card(c['body'])
                layout.addWidget(card)
        else:
            lbl_no_comment = QLabel("Tidak ada komentar.")
            lbl_no_comment.setStyleSheet("font-size: 12px; color: #3d4760; padding: 4px 0;")
            layout.addWidget(lbl_no_comment)

    def _clear_detail_panel(self):
        layout = self.detail_inner_layout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                sub = item.layout()
                while sub.count():
                    w = sub.takeAt(0).widget()
                    if w:
                        w.deleteLater()


    def add_post(self):
        dialog = PostDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.run_worker(
                "create_post", self.on_post_created,
                title=data['title'], body=data['body'],
                author=data['author'], slug=data['slug'], status=data['status']
            )

    def on_post_created(self, result):
        new_id = result.get('data', {}).get('id', '?')
        QMessageBox.information(self, "Sukses", f"Post berhasil dibuat dengan ID: {new_id}")
        self.fetch_posts()


    def edit_post(self):
        row = self.table.currentRow()
        if row < 0:
            return

        post = self.posts_data[row]
        dialog = PostDialog(self, post)

        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.run_worker(
                "update_post", self.on_post_updated,
                post_id=post['id'], title=data['title'], body=data['body'],
                author=data['author'], slug=data['slug'], status=data['status']
            )

    def on_post_updated(self, result):
        QMessageBox.information(self, "Sukses", "Data post berhasil diperbarui!")
        self.fetch_posts()


    def delete_post(self):
        row = self.table.currentRow()
        if row < 0:
            return

        post_id = self.table.item(row, 0).text()
        post_title = self.table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus post '{post_title}'?\n"
            "Tindakan ini juga akan menghapus semua komentar terkait (Cascade).",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.run_worker("delete_post", self.on_post_deleted, post_id=post_id)

    def on_post_deleted(self, result):
        QMessageBox.information(self, "Terhapus", "Post dan komentar terkait telah dihapus.")
        self.fetch_posts()
        self._clear_detail_panel()


    def on_error(self, message):
        self.status_label.setText(f"⚠  {message}")
        self.status_label.setStyleSheet(
            "color: #f87171; font-weight: 600; font-size: 12px; "
            "background: #2a1515; border: 1px solid #5c1515; "
            "border-radius: 6px; padding: 4px 12px;"
        )
        QMessageBox.critical(self, "Terjadi Kesalahan", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = PostViewerApp()
    window.show()
    sys.exit(app.exec())