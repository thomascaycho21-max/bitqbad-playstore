"""Sesion de usuario: guarda en client_storage (local del dispositivo)."""
import json
import flet as ft


class Session:
    KEY = "bitqbad_user"

    def __init__(self, page: ft.Page):
        self.page = page
        self.user = None

    def load(self):
        try:
            raw = self.page.client_storage.get(self.KEY)
            if raw:
                self.user = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            self.user = None
        return self.user

    def save(self, user: dict):
        self.user = user
        try:
            self.page.client_storage.set(self.KEY, json.dumps(user))
        except Exception:
            pass

    def logout(self):
        self.user = None
        try:
            self.page.client_storage.remove(self.KEY)
        except Exception:
            pass

    @property
    def logged_in(self) -> bool:
        return self.user is not None