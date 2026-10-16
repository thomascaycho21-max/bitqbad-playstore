"""Modal de login con token de GitHub."""
import flet as ft
from modules.ui.theme import Theme
from modules.auth.github_auth import GitHubAuth


def open_login_dialog(page: ft.Page, session, on_success):
    token_field = ft.TextField(
        label="Pega tu token de GitHub",
        hint_text="ghp_xxxxxxxxxxxxx",
        password=True,
        can_reveal_password=True,
        bgcolor=Theme.BG_DARK,
        color=Theme.TEXT,
        border_color=Theme.BG_HOVER,
        width=460,
    )
    msg = ft.Text("", size=12)

    def do_login(e):
        try:
            user = GitHubAuth.validate_token(token_field.value)
            session.save(user)
            msg.value = f"Bienvenido, {user['name']}"
            msg.color = Theme.SUCCESS
            page.update()
            import threading, time
            def close():
                time.sleep(0.6)
                page.close(dialog)
                on_success(user)
            threading.Thread(target=close, daemon=True).start()
        except Exception as ex:
            msg.value = f"{ex}"
            msg.color = Theme.DANGER
            page.update()

    def cancel(e):
        page.close(dialog)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOGIN, color=Theme.ACCENT),
                ft.Text("Iniciar sesion con GitHub", color=Theme.TEXT, size=18),
            ],
            spacing=10,
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Para identificarte usa un token personal de GitHub. "
                    "Se guardara solo en este dispositivo.",
                    size=12, color=Theme.TEXT_DIM,
                ),
                ft.Container(height=6),
                token_field,
                ft.TextButton(
                    "Crear token en GitHub →",
                    url="https://github.com/settings/tokens/new?scopes=repo,read:user&description=BitQbad",
                    style=ft.ButtonStyle(color=Theme.ACCENT_2),
                ),
                msg,
            ],
            spacing=6,
            tight=True,
            width=480,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancel,
                          style=ft.ButtonStyle(color=Theme.TEXT_DIM)),
            ft.Button("Entrar", icon=ft.Icons.LOGIN, on_click=do_login,
                              bgcolor=Theme.ACCENT, color=ft.Colors.WHITE),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=Theme.BG_CARD,
    )
    page.open(dialog)