import flet as ft

def view(page: ft.Page):
    return ft.View(
        route="/support",
        controls=[
            ft.Text("Pantalla: Support", size=24)
        ]
    )