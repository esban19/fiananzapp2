import flet as ft

def main(page: ft.Page):
    page.title = "Finanzapp"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 750

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(ft.Text("Menú", size=20, weight="bold"), padding=10),
            ft.NavigationDrawerDestination(icon="person", label="Editar perfil"),
            ft.NavigationDrawerDestination(icon="target", label="Metas"),
            ft.NavigationDrawerDestination(icon="pie_chart", label="Gráficos"),
            ft.NavigationDrawerDestination(icon="school", label="Curso"),
            ft.NavigationDrawerDestination(icon="star", label="Logros"),
            ft.NavigationDrawerDestination(icon="settings", label="Ajustes"),
            ft.NavigationDrawerDestination(icon="help", label="Soporte"),
        ]
    )
    page.drawer = drawer

    def toggle_drawer(e):
        page.drawer.open = not page.drawer.open
        page.update()

    pie_chart = ft.PieChart(
        sections=[
            ft.PieChartSection(value=30, title="Gastos", color="red"),
            ft.PieChartSection(value=40, title="Ingresos", color="green"),
            ft.PieChartSection(value=30, title="Ahorros", color="blue"),
        ],
        width=250,
        height=250,
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Finanzapp"),
            leading=ft.IconButton(icon="menu", on_click=toggle_drawer),
        ),
        ft.Column(
            [
                ft.Text("Total: $1000", size=20),
                ft.Row(
                    [
                        ft.ElevatedButton("Gasto"),
                        ft.ElevatedButton("Ingreso"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                pie_chart,
                ft.Text("¡Ahorra!", size=16, italic=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
    )

ft.app(target=main)
