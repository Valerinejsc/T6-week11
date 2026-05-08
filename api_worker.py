# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

import requests
from PySide6.QtCore import QObject, Signal
from api_service import ApiService

def format_error_message(exc: Exception) -> str:

    if isinstance(exc, requests.exceptions.ConnectionError):
        return "❌ Tidak bisa terhubung ke server"

    if isinstance(exc, requests.exceptions.Timeout):
        return "⏱ Request timeout (lebih dari 10 detik)"

    if isinstance(exc, requests.exceptions.HTTPError):

        code = exc.response.status_code if exc.response else "?"

        if code == 422:

            try:
                error_data = exc.response.json()

                message = (
                    error_data.get("message")
                    or error_data.get("detail")
                    or str(error_data)
                )

            except Exception:
                message = exc.response.text

            return f"⚠ Validasi gagal (422): {message}"

        return f"❌ HTTP Error {code}"

    return f"❌ Error: {str(exc)}"

class ApiWorker(QObject):

    finished = Signal()
    success = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        action,
        post_id=None,
        title=None,
        body=None,
        author=None,
        slug=None,
        status=None
    ):

        super().__init__()

        self.action = action

        self.post_id = post_id
        self.title = title
        self.body = body
        self.author = author
        self.slug = slug
        self.status = status

        self.service = ApiService()

    def run(self):

        try:
            if self.action == "get_posts":

                result = self.service.get_posts()

            elif self.action == "get_post":

                result = self.service.get_post(
                    self.post_id
                )

            elif self.action == "create_post":

                result = self.service.create_post(
                    self.title,
                    self.body,
                    self.author,
                    self.slug,
                    self.status
                )

            elif self.action == "update_post":

                result = self.service.update_post(
                    self.post_id,
                    self.title,
                    self.body,
                    self.author,
                    self.slug,
                    self.status
                )

            elif self.action == "delete_post":

                result = self.service.delete_post(
                    self.post_id
                )

            else:

                raise ValueError(
                    f"Action tidak dikenali: {self.action}"
                )

            self.success.emit(result)

        except Exception as e:

            self.error.emit(
                format_error_message(e)
            )

        finally:

            self.finished.emit()