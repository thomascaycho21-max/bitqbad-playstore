import flet as ft
from modules.ui.theme import Theme


def build(page: ft.Page):
    def feature_card(icon, title, desc, color):
        return Theme.card(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color=color, size=42),
                    ft.Text(title, color=Theme.TEXT, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(desc, color=Theme.TEXT_DIM, size=13),
                ],
                spacing=10,
            ),
            padding=22,
        )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # Hero
            ft.Container(
                padding=30,
                border_radius=Theme.RADIUS_LG,
                gradient=ft.LinearGradient(
                    colors=[Theme.ACCENT, Theme.ACCENT_2],
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                ),
                content=ft.Column(
                    controls=[
                        ft.Text("Bienvenido a BitQbad", size=32,
                                color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Text("Tu tienda de apps multiplataforma",
                                size=16, color=ft.Colors.WHITE),
                        ft.Container(height=14),
                        Theme.button_primary("Explorar tienda", icon=ft.Icons.STORE),
                    ],
                    spacing=6,
                ),
            ),
            ft.Container(height=24),
            # Features
            ft.Text("¿Que puedes hacer?", size=20, color=Theme.TEXT,
                    weight=ft.FontWeight.BOLD),
            ft.Container(height=12),
            ft.Row(
                controls=[
                    feature_card(ft.Icons.APPS, "Descubrir",
                                 "Apps para todas las plataformas", Theme.ACCENT),
                    feature_card(ft.Icons.RATE_REVIEW, "Reseñar",
                                 "Comparte tu opinion con la comunidad", Theme.ACCENT_2),
                    feature_card(ft.Icons.MONETIZATION_ON, "Ganar monedas",
                                 "Vi ads, comparte y suscribete", Theme.ACCENT_3),
                ],
                spacing=16,
            ),
        ],
    )
