"""
BitQbad PlayStore - Entry point
- Desktop: ventana nativa
- Web (Render): servidor web con puerto $PORT
"""
import os
import sys
import traceback

# Cargar .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import flet as ft

# Directorio base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def main(page: ft.Page):
    try:
        _run(page)
    except Exception as e:
        tb = traceback.format_exc()
        page.bgcolor = "#0D0D0F"
        page.add(
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("ERROR AL INICIAR LA APP", size=20,
                                color="#FF1744", weight=ft.FontWeight.BOLD),
                        ft.Text(str(e), size=14, color="#FFAB00"),
                        ft.Container(height=10),
                        ft.Container(
                            padding=12,
                            bgcolor="#1A1A1F",
                            border_radius=8,
                            content=ft.Text(tb, size=11, color="#A0A0A8",
                                            font_family="Consolas",
                                            selectable=True),
                        ),
                    ],
                ),
            )
        )
        print("ERROR AL INICIAR:\n" + tb)


def _run(page: ft.Page):
    from modules.ui.theme import Theme
    from modules.ui.router import Router
    from modules.ui.layout import Layout
    from modules.store.repository import StoreRepository
    from modules.auth.session import Session

    from views import home_view, store_view, reviews_view, coins_view, about_view
    from views import app_detail_view

    page.title = "BitQbad PlayStore"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = Theme.BG_DARK
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 900
    page.window.min_height = 600

    repo = StoreRepository(os.path.join(BASE_DIR, "database", "apps.json"))

    session = Session(page)
    session.load()

    state = {"selected_app_id": None}

    router = Router(page, container=ft.Container(expand=True))
    layout = Layout(page, router, session=session)
    router.container = layout.content_area
    router.on_change = lambda name: layout.set_highlight(
        "store" if name == "app-detail" else name
    )

    router.register("home",    home_view.build)
    router.register("store",   store_view.build)
    router.register("reviews", reviews_view.build)
    router.register("coins",   coins_view.build)
    router.register("about",   about_view.build)

    def build_app_detail(p):
        app_id = state.get("selected_app_id")
        app = repo.by_id(app_id) if app_id else None
        if not app:
            return ft.Text("App no encontrada", color=Theme.DANGER)
        return app_detail_view.build(p, app, router)

    router.register("app-detail", build_app_detail)

    page._bitqbad_state = state
    page._bitqbad_router = router
    page._bitqbad_session = session

    page.add(layout.root)
    layout.refresh_user_area()
    router.go("home")


if __name__ == "__main__":
    # Si estamos en Render (variable PORT) -> modo web
    port = os.getenv("PORT") or os.getenv("FLET_SERVER_PORT")

    if port:
        print(f"[BitQbad] Iniciando en modo WEB puerto {port}")
        ft.run(
            main,
            view=ft.AppView.WEB_BROWSER,
            port=int(port),
            host="0.0.0.0",
        )
    else:
        print("[BitQbad] Iniciando en modo DESKTOP")
        ft.run(main)