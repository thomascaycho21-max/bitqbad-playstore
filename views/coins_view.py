"""Vista de Monedas tipo Robux."""
import os
import flet as ft
from modules.ui.theme import Theme
from modules.coins.service import CoinsService


# Codigos de canje (compartir/sub)
SHARE_REWARD = 20
AD_REWARD    = 10
SUB_REWARD   = 50
WELCOME      = 100


def build(page: ft.Page):
    service = CoinsService()

    # Usuario actual (desde session en page._bitqbad_session si existe)
    session = getattr(page, "_bitqbad_session", None)
    user = (session.user.get("login") if session and session.user else "anon")

    # ------- Estado UI -------
    balance_text = ft.Text("0", size=44, color=Theme.TEXT, weight=ft.FontWeight.BOLD)
    msg = ft.Text("", size=13)

    def refresh():
        w = service.get_wallet(user)
        balance_text.value = str(w.balance)
        page.update()

    def reward(amount: int, reason: str):
        w = service.add_coins(user, amount, reason)
        msg.value = f"+{amount} monedas ({reason}). Total: {w.balance}"
        msg.color = Theme.SUCCESS
        refresh()

    # ------- Acciones -------
    def on_see_ad(e):
        reward(AD_REWARD, "Ver anuncio")

    def on_share(e):
        url = "https://bitqbad-playstore.onrender.com"
        page.launch_url(f"https://twitter.com/intent/tweet?url={url}")
        reward(SHARE_REWARD, "Compartir")

    def on_subscribe(e):
        page.launch_url("https://www.youtube.com/@bitqbad")
        reward(SUB_REWARD, "Suscribirse al canal")

    def on_buy(e):
        page.open(ft.SnackBar(
            ft.Text("Compras con Stripe/PayPal — proximamente"),
            bgcolor=Theme.WARNING,
        ))

    # ------- Cards -------
    def action_card(icon, title, desc, reward_text, color, handler):
        return ft.Container(
            on_click=handler,
            padding=20,
            bgcolor=Theme.BG_CARD,
            border_radius=Theme.RADIUS_MD,
            ink=True,
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color=color, size=42),
                    ft.Text(title, size=16, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
                    ft.Text(desc, size=12, color=Theme.TEXT_DIM),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Text(reward_text, size=13, color=color,
                                        weight=ft.FontWeight.BOLD),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                        bgcolor=Theme.BG_HOVER,
                        border_radius=Theme.RADIUS_SM,
                    ),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # ------- Header (cartera) -------
    header = ft.Container(
        padding=24,
        border_radius=Theme.RADIUS_LG,
        gradient=ft.LinearGradient(
            colors=[Theme.ACCENT_3, Theme.ACCENT],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
        ),
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.WHITE, size=64),
                ft.Column(
                    controls=[
                        ft.Text("Tu cartera", size=16, color=ft.Colors.WHITE),
                        ft.Row(
                            controls=[
                                balance_text,
                                ft.Text("monedas", size=16, color=ft.Colors.WHITE),
                            ],
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        ),
                        ft.Text(f"Usuario: {user}", size=12, color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE)),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            spacing=20,
        ),
    )

    # ------- Estado del backend GitHub -------
    backend_status = ft.Text(
        "Sincronizacion con GitHub: ACTIVA" if service.enabled
        else f"Sincronizacion con GitHub: OFF ({service.error or 'sin config'})",
        size=12,
        color=Theme.SUCCESS if service.enabled else Theme.WARNING,
    )

    # ------- Ganar monedas -------
    earn_row = ft.Row(
        controls=[
            action_card(ft.Icons.ONDEMAND_VIDEO, "Ver anuncio",
                        "Mira un video corto",
                        f"+{AD_REWARD} monedas", Theme.ACCENT_2, on_see_ad),
            action_card(ft.Icons.SHARE, "Compartir",
                        "Comparte en redes",
                        f"+{SHARE_REWARD} monedas", Theme.SUCCESS, on_share),
            action_card(ft.Icons.SUBSCRIPTIONS, "Suscribirse",
                        "Al canal de YouTube",
                        f"+{SUB_REWARD} monedas", Theme.ACCENT_3, on_subscribe),
        ],
        spacing=16,
    )

    buy_row = ft.Row(
        controls=[
            action_card(ft.Icons.SHOPPING_CART, "Comprar monedas",
                        "Con Stripe / PayPal",
                        "Proximamente", Theme.ACCENT, on_buy),
        ],
        spacing=16,
    )

    # ------- Historial -------
    history_col = ft.Column(spacing=6)

    def refresh_history():
        history_col.controls.clear()
        w = service.get_wallet(user)
        txs = w.transactions[-10:] if w.transactions else []
        if not txs:
            history_col.controls.append(
                ft.Text("Sin movimientos aun.", color=Theme.TEXT_DIM, size=12)
            )
        else:
            for t in reversed(txs):
                sign = "+" if t.amount >= 0 else ""
                color = Theme.SUCCESS if t.amount >= 0 else Theme.DANGER
                history_col.controls.append(
                    ft.Container(
                        padding=10,
                        bgcolor=Theme.BG_HOVER,
                        border_radius=Theme.RADIUS_SM,
                        content=ft.Row(
                            controls=[
                                ft.Text(f"{sign}{t.amount}", size=13, color=color,
                                        weight=ft.FontWeight.BOLD, width=60),
                                ft.Text(t.reason, size=13, color=Theme.TEXT, expand=True),
                                ft.Text(t.timestamp[:16].replace("T", " "),
                                        size=11, color=Theme.TEXT_DIM),
                            ],
                        ),
                    )
                )

    def reload_all():
        refresh()
        refresh_history()

    # Wire refresh into reward
    _orig_reward = reward
    def reward(amount, reason):
        _orig_reward(amount, reason)
        refresh_history()
        page.update()

    reload_all()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Monedas", size=28, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Container(height=12),
            header,
            ft.Container(height=8),
            backend_status,
            ft.Container(height=24),
            ft.Text("Gana monedas", size=18, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            earn_row,
            ft.Container(height=24),
            ft.Text("Compra monedas", size=18, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            buy_row,
            ft.Container(height=24),
            ft.Text("Historial", size=18, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            history_col,
            ft.Container(height=20),
            msg,
        ],
        spacing=0,
    )