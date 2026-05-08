# Nama : Valerine Jesika Dewi
# NIM  : F1D02310027

import requests

class ApiService:
    BASE_URL = "https://api.pahrul.my.id/api"
    TIMEOUT = 10

    def _safe_request(self, func, *args, **kwargs):
        try:
            response = func(*args, **kwargs, timeout=self.TIMEOUT)
            
            if response.status_code == 422:
                error_data = response.json()
                raise Exception(f"Validasi Gagal: {error_data.get('message', 'Data tidak valid')}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("Koneksi gagal: Waktu tunggu (timeout) habis.")
        except requests.exceptions.ConnectionError:
            raise Exception("Koneksi gagal: Periksa koneksi internet Anda.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Server Error: {e.response.status_code}")

    def get_posts(self):
        data = self._safe_request(requests.get, f"{self.BASE_URL}/posts")
        return data.get("data", data) if isinstance(data, dict) else data

    def get_post(self, post_id):
        data = self._safe_request(requests.get, f"{self.BASE_URL}/posts/{post_id}")
        return data.get("data", data)

    def create_post(self, title, body, author, slug, status):
        payload = {"title": title, "body": body, "author": author, "slug": slug, "status": status}
        return self._safe_request(requests.post, f"{self.BASE_URL}/posts", json=payload)

    def update_post(self, post_id, title, body, author, slug, status):
        payload = {"title": title, "body": body, "author": author, "slug": slug, "status": status}
        return self._safe_request(requests.put, f"{self.BASE_URL}/posts/{post_id}", json=payload)

    def delete_post(self, post_id):
        self._safe_request(requests.delete, f"{self.BASE_URL}/posts/{post_id}")
        return True
