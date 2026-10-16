"""Router simple: cambia la vista activa sin recargar la pagina."""
import flet as ft


class Router:
    def __init__(self, page: ft.Page, container: ft.Container):
        self.page = page
        self.container = container
        self.routes = {}          # nombre -> funcion(page) -> Control
        self.current = None
        self.on_change = None     # callback(nombre)

    def register(self, name, builder):
        """builder(page) debe devolver un ft.Control."""
        self.routes[name] = builder

    def go(self, name: str):
        if name not in self.routes:
            print(f"[Router] Ruta no encontrada: {name}")
            return
        self.current = name
        view = self.routes[name](self.page)
        self.container.content = view
        if self.on_change:
            self.on_change(name)
        self.page.update()
