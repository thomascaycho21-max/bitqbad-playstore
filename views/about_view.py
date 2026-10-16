import flet as ft
from modules.ui.theme import Theme


def build(page: ft.Page):
    return ft.Column(
        controls=[
            ft.Text("Acerca de", size=28, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            Theme.card(
                content=ft.Column(
                    controls=[
                        ft.Text("BitQbad PlayStore", size=22, color=Theme.TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Text("Version 0.1.2", color=Theme.TEXT_DIM, size=14),
                        ft.Container(height=8),
                        ft.Text("App multiplataforma hecha con Flet.",
                                color=Theme.TEXT, size=14),
                        ft.Text("Windows · Linux · macOS · Android · iOS · Web",
                                color=Theme.TEXT_DIM, size=13),
                    ],
                    spacing=6,
                ),
                padding=28,
            ),
        ],
    )
