import flet as ft

def view(page: ft.Page):
    return ft.View(
        route="/expenses",
        controls=[
            ft.Text("Pantalla: Expenses", size=24)
        ]
    )