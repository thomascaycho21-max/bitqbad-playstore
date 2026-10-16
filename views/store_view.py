"""Vista Store: grid de apps con filtros y busqueda."""
import os
import flet as ft
from modules.ui.theme import Theme
from modules.store.repository import StoreRepository


_REPO = None


def _get_repo():
    global _REPO
    if _REPO is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _REPO = StoreRepository(os.path.join(base, "database", "apps.json"))
    return _REPO


def build(page: ft.Page):
    repo = _get_repo()

    state = {"category": "Todas", "query": ""}

    grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=320,
        child_aspect_ratio=1.15,
        spacing=16,
        run_spacing=16,
    )

    counter = ft.Text("", size=13, color=Theme.TEXT_DIM)

    def app_card(app):
        def on_click(e):
            # Guardar en atributo del page (no existe page.session)
            try:
                page._bitqbad_state["selected_app_id"] = app.id
                page._bitqbad_router.go("app-detail")
            except Exception as ex:
                page.open(ft.SnackBar(
                    ft.Text(f"Error: {ex}"),
                    bgcolor=Theme.DANGER,
                ))

        return Theme.card(
            on_click=on_click,
            padding=16,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=56, height=56,
                                bgcolor=app.icon_color,
                                border_radius=14,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Text(app.icon_emoji, size=30),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(app.name, size=15, color=Theme.TEXT,
                                            weight=ft.FontWeight.BOLD,
                                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(app.category, size=12, color=Theme.TEXT_DIM),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=8),
                    ft.Text(app.short_desc, size=12, color=Theme.TEXT_DIM,
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.STAR, size=14, color=Theme.WARNING),
                            ft.Text(f"{app.rating:.1f}", size=12, color=Theme.TEXT),
                            ft.Container(expand=True),
                            ft.Text(f"{app.downloads_str()} ⬇", size=12, color=Theme.TEXT_DIM),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=0,
            ),
        )

    def refresh_grid():
        grid.controls.clear()
        results = repo.filter(category=state["category"], query=state["query"])
        for app in results:
            grid.controls.append(app_card(app))
        counter.value = f"{len(results)} app(s) encontradas"
        page.update()

    def on_search(e):
        state["query"] = e.control.value
        refresh_grid()

    search = ft.TextField(
        hint_text="Buscar apps...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=Theme.RADIUS_MD,
        bgcolor=Theme.BG_CARD,
        border_color=Theme.BG_HOVER,
        color=Theme.TEXT,
        on_change=on_search,
        expand=True,
    )

    category_row = ft.Row(spacing=8, wrap=True)

    def make_cat_chip(cat):
        def on_click(e):
            state["category"] = cat
            for c in category_row.controls:
                is_active = c.data == cat
                c.bgcolor = Theme.ACCENT if is_active else Theme.BG_CARD
                c.content.color = Theme.TEXT if is_active else Theme.TEXT_DIM
            refresh_grid()

        return ft.Container(
            data=cat,
            content=ft.Text(cat, size=13,
                            color=Theme.ACCENT if cat == "Todas" else Theme.TEXT_DIM),
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            bgcolor=Theme.ACCENT if cat == "Todas" else Theme.BG_CARD,
            border_radius=Theme.RADIUS_SM,
            on_click=on_click,
            ink=True,
        )

    for cat in repo.categories:
        category_row.controls.append(make_cat_chip(cat))

    refresh_grid()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Tienda", size=28, color=Theme.TEXT,
                            weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    counter,
                ],
            ),
            ft.Container(height=12),
            search,
            ft.Container(height=12),
            category_row,
            ft.Container(height=16),
            grid,
        ],
        spacing=0,
        expand=True,
    )