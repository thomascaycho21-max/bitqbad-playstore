"""Vista detalle de una app + reseñas."""
import flet as ft
from modules.ui.theme import Theme
from modules.reviews.service import ReviewsService


def _stars(rating, size=14):
    rating = int(round(rating))
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


def build(page: ft.Page, app, router):
    service = ReviewsService()

    # -------- Header --------
    def info_chip(icon, text, color=None):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=16, color=color or Theme.TEXT_DIM),
                    ft.Text(text, size=13, color=Theme.TEXT_DIM),
                ],
                spacing=6,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            bgcolor=Theme.BG_HOVER,
            border_radius=Theme.RADIUS_SM,
        )

    def platform_chip(name):
        return ft.Container(
            content=ft.Text(name, size=12, color=Theme.TEXT),
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            bgcolor=Theme.BG_HOVER,
            border_radius=Theme.RADIUS_SM,
        )

    def on_download(e):
        if app.download_url:
            page.launch_url(app.download_url)
        else:
            page.open(ft.SnackBar(ft.Text("Sin URL de descarga"), bgcolor=Theme.WARNING))

    def on_repo(e):
        if app.repo_url:
            page.launch_url(app.repo_url)

    header = ft.Container(
        padding=24,
        border_radius=Theme.RADIUS_LG,
        gradient=ft.LinearGradient(
            colors=[app.icon_color, Theme.BG_CARD],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
        ),
        content=ft.Row(
            controls=[
                ft.Container(
                    width=90, height=90,
                    bgcolor=app.icon_color,
                    border_radius=22,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(app.icon_emoji, size=48),
                ),
                ft.Column(
                    controls=[
                        ft.Text(app.name, size=26, color=Theme.TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(app.short_desc, size=14, color=Theme.TEXT),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STAR, size=16, color=Theme.WARNING),
                                ft.Text(f"{app.rating:.1f}", size=13, color=Theme.TEXT),
                                ft.Text("·", size=13, color=Theme.TEXT_DIM),
                                ft.Text(f"{app.downloads_str()} descargas",
                                        size=13, color=Theme.TEXT_DIM),
                                ft.Text("·", size=13, color=Theme.TEXT_DIM),
                                ft.Text(f"{app.size_mb} MB", size=13, color=Theme.TEXT_DIM),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
            ],
            spacing=20,
        ),
    )

    actions = ft.Row(
        controls=[
            Theme.button_primary("Descargar", icon=ft.Icons.DOWNLOAD, on_click=on_download),
            Theme.button_ghost("GitHub", icon=ft.Icons.CODE, on_click=on_repo),
        ],
        spacing=12,
    )

    chips = ft.Row(
        controls=[
            info_chip(ft.Icons.CATEGORY, app.category, Theme.ACCENT),
            info_chip(ft.Icons.LABEL, f"v{app.version}"),
        ],
        spacing=8, wrap=True,
    )

    platforms = ft.Column(
        controls=[
            ft.Text("Plataformas", size=15, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[platform_chip(p) for p in app.platforms], spacing=8, wrap=True),
        ],
        spacing=8,
    )

    desc = ft.Column(
        controls=[
            ft.Text("Descripcion", size=15, color=Theme.TEXT, weight=ft.FontWeight.BOLD),
            ft.Text(app.long_desc or app.short_desc, size=14, color=Theme.TEXT_DIM),
        ],
        spacing=8,
    )

    # -------- SECCION RESEÑAS --------
    reviews_col = ft.Column(spacing=10)
    avg_text = ft.Text("", size=13, color=Theme.TEXT_DIM)

    # Formulario
    name_field = ft.TextField(label="Tu nombre", value="anon", width=200,
                              bgcolor=Theme.BG_CARD, color=Theme.TEXT)
    rating_field = ft.Dropdown(
        label="Puntuacion",
        value="5",
        width=140,
        bgcolor=Theme.BG_CARD, color=Theme.TEXT,
        options=[ft.DropdownOption(str(i), f"{i} ⭐") for i in range(5, 0, -1)],
    )
    title_field = ft.TextField(label="Titulo", bgcolor=Theme.BG_CARD,
                                color=Theme.TEXT, expand=True)
    body_field = ft.TextField(
        label="Comentario", multiline=True, min_lines=3, max_lines=6,
        bgcolor=Theme.BG_CARD, color=Theme.TEXT, expand=True,
    )
    msg = ft.Text("", size=12)

    def reload_reviews():
        reviews_col.controls.clear()
        revs = service.list_for(app.id, force=True)
        avg = service.average_rating(app.id)
        avg_text.value = f"{len(revs)} reseña(s) · promedio {avg:.1f}/5" if revs else "Sin reseñas aun"

        if not revs:
            reviews_col.controls.append(
                ft.Text("Se el primero en opinar.", color=Theme.TEXT_DIM, size=13)
            )
        else:
            for r in revs:
                reviews_col.controls.append(
                    Theme.card(
                        padding=14,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE,
                                                color=Theme.ACCENT, size=26),
                                        ft.Text(r.user, size=13, color=Theme.TEXT,
                                                weight=ft.FontWeight.BOLD),
                                        ft.Container(expand=True),
                                        _stars(r.rating, size=12),
                                    ],
                                    spacing=6,
                                ),
                                ft.Text(r.title, size=14, color=Theme.TEXT),
                                ft.Text(r.body, size=12, color=Theme.TEXT_DIM),
                            ],
                            spacing=4,
                        ),
                    )
                )
        page.update()

    def submit_review(e):
        if not service.enabled:
            msg.value = "GitHub no configurado (.env)"
            msg.color = Theme.DANGER
            page.update()
            return
        if not title_field.value or not body_field.value:
            msg.value = "Rellena titulo y comentario"
            msg.color = Theme.WARNING
            page.update()
            return
        try:
            service.add(
                app_id=app.id,
                title=title_field.value,
                body=body_field.value,
                rating=int(rating_field.value),
                user=name_field.value or "anon",
            )
            msg.value = "✅ Reseña publicada en GitHub"
            msg.color = Theme.SUCCESS
            title_field.value = ""
            body_field.value = ""
            reload_reviews()
        except Exception as ex:
            msg.value = f"❌ Error: {ex}"
            msg.color = Theme.DANGER
            page.update()

    form = Theme.card(
        padding=16,
        content=ft.Column(
            controls=[
                ft.Text("Escribe una reseña", size=15, color=Theme.TEXT,
                        weight=ft.FontWeight.BOLD),
                ft.Row(controls=[name_field, rating_field], spacing=10),
                title_field,
                body_field,
                ft.Row(
                    controls=[
                        ft.Button(
                            "Publicar",
                            icon=ft.Icons.SEND,
                            on_click=submit_review,
                            bgcolor=Theme.ACCENT,
                            color=ft.Colors.WHITE,
                        ),
                        msg,
                    ],
                    spacing=12,
                ),
            ],
            spacing=10,
        ),
    )

    back = ft.TextButton(
        "← Volver a la tienda",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: router.go("store"),
        style=ft.ButtonStyle(color=Theme.TEXT_DIM),
    )

    reviews_section = Theme.card(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Reseñas", size=16, color=Theme.TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        avg_text,
                    ],
                ),
                ft.Container(height=10),
                form,
                ft.Container(height=14),
                reviews_col,
            ],
            spacing=0,
        ),
    )

    # Cargar reseñas al inicio
    reload_reviews()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            back,
            ft.Container(height=8),
            header,
            ft.Container(height=20),
            actions,
            ft.Container(height=20),
            chips,
            ft.Container(height=8),
            Theme.card(
                content=ft.Column(controls=[platforms, ft.Container(height=14), desc],
                                  spacing=14),
                padding=20,
            ),
            ft.Container(height=20),
            reviews_section,
        ],
        spacing=0,
    )