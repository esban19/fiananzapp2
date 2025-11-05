import flet as ft

def view(page: ft.Page):
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(ft.Text("Menú", size=20, weight="bold"), padding=10),
            ft.NavigationDrawerDestination(icon="person", label="Perfil"),
            ft.NavigationDrawerDestination(icon="flag", label="Metas"),
            ft.NavigationDrawerDestination(icon="pie_chart", label="Gráficos"),
            ft.NavigationDrawerDestination(icon="school", label="Curso"),
            ft.NavigationDrawerDestination(icon="star", label="Logros"),
            ft.NavigationDrawerDestination(icon="settings", label="Ajustes"),
            ft.NavigationDrawerDestination(icon="help", label="Soporte"),
        ],
        on_change=lambda e: page.go([
            "/profile", "/metas", "/charts", "/course", "/achievements", "/settings", "/support"
        ][e.control.selected_index])
    )
    
    achievements = [
        {"title": "Curso inicial completado", "icon": "check_circle", "desc": "Has completado tu primer curso"},
        {"title": "Meta de ahorro alcanzada", "icon": "savings", "desc": "Ahorraste $500"},
        {"title": "Usuario constante", "icon": "calendar_today", "desc": "Ingresaste 7 días seguidos"},
    ]

    def open_drawer(e):
        drawer.open = True
        page.update()

    return ft.View(
        route="/achievments",
        drawer=drawer,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.AppBar(
                title=ft.Text("Finanzapp"),
                leading=ft.IconButton(icon="menu", on_click=open_drawer)
            ),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(a["icon"], color="gold"),
                        title=ft.Text(a["title"]),
                        subtitle=ft.Text(a["desc"]),
                    ) for a in achievements
                ]
            )
        ]
    )
