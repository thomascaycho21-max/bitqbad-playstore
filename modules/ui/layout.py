"""Layout principal: sidebar + header con login + contenido."""
import flet as ft
from .theme import Theme


class Layout:
    def __init__(self, page: ft.Page, router, session=None):
        self.page = page
        self.router = router
        self.session = session
        self.content_area = ft.Container(expand=True, padding=Theme.PAD_LG)
        self.nav_buttons = {}
        self.user_area = ft.Container()
        self._build()

    # ---------- Nav ----------
    def _nav_item(self, name, icon, label):
        btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=Theme.TEXT_DIM, size=22),
                    ft.Text(label, color=Theme.TEXT_DIM, size=15),
                ],
                spacing=14,
            ),
            padding=ft.Padding.symmetric(horizontal=18, vertical=14),
            border_radius=Theme.RADIUS_MD,
            on_click=lambda e, n=name: self.router.go(n),
            ink=True,
        )
        self.nav_buttons[name] = btn
        return btn

    def _highlight(self, active_name):
        for name, btn in self.nav_buttons.items():
            row = btn.content
            icon = row.controls[0]
            text = row.controls[1]
            if name == active_name:
                btn.bgcolor = Theme.BG_HOVER
                icon.color = Theme.ACCENT
                text.color = Theme.TEXT
            else:
                btn.bgcolor = None
                icon.color = Theme.TEXT_DIM
                text.color = Theme.TEXT_DIM

    # ---------- User ----------
    def refresh_user_area(self):
        try:
            if self.session and self.session.logged_in:
                u = self.session.user
                avatar_url = u.get("avatar") or None
                initial = (u.get("name") or u.get("login") or "?")[0].upper()
                self.user_area.content = ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            foreground_image_src=avatar_url,
                            content=ft.Text(initial, color=ft.Colors.WHITE),
                            bgcolor=Theme.ACCENT,
                            radius=18,
                        ),
                        ft.Text(u.get("name") or u.get("login"),
                                color=Theme.TEXT, size=14),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_color=Theme.TEXT_DIM,
                            tooltip="Cerrar sesion",
                            on_click=self._on_logout,
                        ),
                    ],
                    spacing=10,
                )
            else:
                self.user_area.content = ft.Button(
                    "Iniciar sesion",
                    icon=ft.Icons.LOGIN,
                    on_click=self._on_login,
                    bgcolor=Theme.ACCENT,
                    color=ft.Colors.WHITE,
                )
            self.page.update()
        except Exception:
            pass

    def _on_login(self, e):
        from views.login_view import open_login_dialog
        open_login_dialog(self.page, self.session,
                          on_success=lambda u: self.refresh_user_area())

    def _on_logout(self, e):
        if self.session:
            self.session.logout()
        self.refresh_user_area()

    # ---------- Build ----------
    def _build(self):
        sidebar = ft.Container(
            width=230,
            bgcolor=Theme.SIDEBAR,
            padding=ft.Padding.symmetric(vertical=20, horizontal=12),
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.Padding.only(left=10, bottom=30),
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.APPS, color=Theme.ACCENT, size=32),
                                ft.Text("BitQbad", color=Theme.TEXT, size=22,
                                        weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10,
                        ),
                    ),
                    self._nav_item("home",    ft.Icons.HOME,           "Inicio"),
                    self._nav_item("store",   ft.Icons.STORE,          "Tienda"),
                    self._nav_item("reviews", ft.Icons.RATE_REVIEW,    "Reseñas"),
                    self._nav_item("coins",   ft.Icons.MONETIZATION_ON,"Monedas"),
                    self._nav_item("about",   ft.Icons.INFO,           "Acerca de"),
                    ft.Container(expand=True),
                    ft.Container(
                        padding=ft.Padding.only(left=10),
                        content=ft.Text("v0.1.5", color=Theme.TEXT_DIM, size=12),
                    ),
                ],
                spacing=6,
            ),
        )

        header = ft.Container(
            padding=ft.Padding.symmetric(horizontal=24, vertical=14),
            bgcolor=Theme.BG_DARK,
            content=ft.Row(
                controls=[
                    ft.Text("BitQbad PlayStore", color=Theme.TEXT,
                            size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=Theme.TEXT_DIM),
                    self.user_area,
                ],
                spacing=14,
            ),
        )

        self.root = ft.Row(
            controls=[
                sidebar,
                ft.Column(
                    expand=True,
                    controls=[
                        header,
                        ft.Divider(height=1, color=Theme.BG_HOVER),
                        self.content_area,
                    ],
                    spacing=0,
                ),
            ],
            spacing=0,
            expand=True,
        )

        self.refresh_user_area()

    def set_highlight(self, name):
        self._highlight(name)
        try:
            self.page.update()
        except Exception:
            pass