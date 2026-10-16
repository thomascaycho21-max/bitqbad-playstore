"""Paleta y estilos globales de BitQbad PlayStore."""
import flet as ft


class Theme:
    # Colores principales
    BG_DARK      = "#0D0D0F"
    BG_CARD      = "#1A1A1F"
    BG_HOVER     = "#25252B"
    SIDEBAR      = "#121216"
    ACCENT       = "#7C4DFF"   # morado BitQbad
    ACCENT_2     = "#00E5FF"   # cyan
    ACCENT_3     = "#FF4081"   # rosa
    TEXT         = "#FFFFFF"
    TEXT_DIM     = "#A0A0A8"
    SUCCESS      = "#00E676"
    WARNING      = "#FFAB00"
    DANGER       = "#FF1744"

    # Espaciados
    PAD_SM = 8
    PAD_MD = 16
    PAD_LG = 24

    # Radios
    RADIUS_SM = 8
    RADIUS_MD = 14
    RADIUS_LG = 22

    @staticmethod
    def card(content, padding=16, on_click=None, bg=None):
        """Card con estilo consistente."""
        return ft.Container(
            content=content,
            padding=padding,
            bgcolor=bg or Theme.BG_CARD,
            border_radius=Theme.RADIUS_MD,
            on_click=on_click,
            ink=bool(on_click),
        )

    @staticmethod
    def button_primary(text, on_click=None, icon=None):
        return ft.Button(
            content=text,
            icon=icon,
            on_click=on_click,
            bgcolor=Theme.ACCENT,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS_MD),
                padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            ),
        )

    @staticmethod
    def button_ghost(text, on_click=None, icon=None):
        return ft.OutlinedButton(
            content=text,
            icon=icon,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=Theme.TEXT,
                side=ft.BorderSide(1, Theme.BG_HOVER),
                shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS_MD),
                padding=ft.Padding.symmetric(horizontal=20, vertical=14),
            ),
        )
