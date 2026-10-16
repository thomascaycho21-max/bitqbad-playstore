"""Vista de reseñas general + por app."""
import os
import flet as ft
from modules.ui.theme import Theme
from modules.reviews.service import ReviewsService
from modules.store.repository import StoreRepository


_SERVICE = None
_REPO = None


def _get_service():
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = ReviewsService()
    return _SERVICE


def _get_store():
    global _REPO
    if _REPO is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _REPO = StoreRepository(os.path.join(base, "database", "apps.json"))
    return _REPO


def _stars(rating: int, size=14):
    return ft.Row(
        spacing=2,
        controls=[
            ft.Icon(
                ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER,
                color=Theme.WARNING if i < rating else Theme.TEXT_DIM,
                size=size,
            )
            for i in range(5)
        ],
    )


def _review_card(rev):
    return Theme.card(
        padding=16,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=Theme.ACCENT, size=32),
                        ft.Column(
                            controls=[
                                ft.Text(rev.user, size=14, color=Theme.TEXT,
                                        weight=ft.FontWeight.BOLD),
                                _stars(rev.rating),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Text(rev.created_at[:10] if rev.created_at else "",
                                size=11, color=Theme.TEXT_DIM),
                    ],
                    spacing=10,
                ),
                ft.Container(height=8),
                ft.Text(rev.title, size=15, color=Theme.TEXT,
                        weight=ft.FontWeight.BOLD),
                ft.Text(rev.body, size=13, color=Theme.TEXT_DIM),
            ],
            spacing=4,
        ),
    )


def build(page: ft.Page):
    service = _get_service()
    store = _get_store()

    state = {"app_id": "todas"}
    reviews_col = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    status_text = ft.Text("", size=13, color=Theme.TEXT_DIM)

    def show_config_error():
        reviews_col.controls.clear()
        reviews_col.controls.append(
            Theme.card(
                padding=24,
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.WARNING_AMBER, color=Theme.WARNING, size=48),
                        ft.Text("GitHub no configurado", size=18,
                                color=Theme.TEXT, weight=ft.FontWeight.BOLD),
                        ft.Text("Diagnostico:", size=13, color=Theme.TEXT_DIM),
                        ft.Container(
                            padding=12,
                            bgcolor=Theme.BG_HOVER,
                            border_radius=Theme.RADIUS_SM,
                            content=ft.Text(
                                service.error or "Sin detalle del error",
                                size=12, color=Theme.DANGER,
                                font_family="Consolas",
                                selectable=True,
                            ),
                        ),
                        ft.Container(height=8),
                        ft.Text("Como arreglar:", size=14, color=Theme.TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Text("1. Abre el archivo .env", size=13, color=Theme.TEXT_DIM),
                        ft.Text("2. Pon GITHUB_TOKEN=ghp_... (token valido)", size=13,
                                color=Theme.TEXT_DIM),
                        ft.Text("3. Pon GITHUB_REPO=usuario/repositorio (debe existir)", size=13,
                                color=Theme.TEXT_DIM),
                        ft.Text("4. Cierra y vuelve a abrir la app", size=13,
                                color=Theme.TEXT_DIM),
                        ft.Container(height=10),
                        ft.TextButton(
                            "Crear token en GitHub →",
                            url="https://github.com/settings/tokens/new?scopes=repo,read:user",
                            style=ft.ButtonStyle(color=Theme.ACCENT_2),
                        ),
                    ],
                    spacing=6,
                ),
            )
        )
        status_text.value = "Sin conexion a GitHub"
        status_text.color = Theme.DANGER
        page.update()

    def refresh(force=False):
        reviews_col.controls.clear()
        if not service.enabled:
            show_config_error()
            return

        app_ids = [state["app_id"]] if state["app_id"] != "todas" \
                  else [a.id for a in store.all()]

        total = 0
        for app_id in app_ids:
            revs = service.list_for(app_id, force=force)
            if not revs:
                continue
            app = store.by_id(app_id)
            app_name = app.name if app else app_id
            reviews_col.controls.append(
                ft.Text(f"Reseñas de {app_name}", size=16,
                        color=Theme.TEXT, weight=ft.FontWeight.BOLD)
            )
            for r in revs:
                reviews_col.controls.append(_review_card(r))
                total += 1
            reviews_col.controls.append(ft.Container(height=8))

        if total == 0:
            reviews_col.controls.append(
                Theme.card(
                    padding=30,
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RATE_REVIEW, color=Theme.ACCENT_2, size=48),
                            ft.Text("Aun no hay reseñas", size=16, color=Theme.TEXT),
                            ft.Text("Ve a una app y escribe la primera.",
                                    size=13, color=Theme.TEXT_DIM),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6,
                    ),
                )
            )

        status_text.value = f"{total} reseña(s)"
        status_text.color = Theme.TEXT_DIM
        page.update()

    # Filtro
    options = [ft.DropdownOption(key="todas", content="Todas las apps")]
    for a in store.all():
        options.append(ft.DropdownOption(key=a.id, content=a.name))

    def on_app_change(e):
        state["app_id"] = e.control.value
        refresh(force=True)

    app_filter = ft.Dropdown(
        options=options, value="todas", width=280,
        bgcolor=Theme.BG_CARD, color=Theme.TEXT, border_color=Theme.BG_HOVER,
        on_select=on_app_change,
    )

    refresh_btn = ft.IconButton(
        icon=ft.Icons.REFRESH, icon_color=Theme.TEXT,
        tooltip="Recargar desde GitHub",
        on_click=lambda e: refresh(force=True),
    )

    refresh()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Reseñas", size=28, color=Theme.TEXT,
                            weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    status_text,
                ],
            ),
            ft.Container(height=12),
            ft.Row(controls=[app_filter, refresh_btn], spacing=12),
            ft.Container(height=16),
            reviews_col,
        ],
        spacing=0,
        expand=True,
    )