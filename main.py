import flet as ft
from screens import login, dashboard, expenses, charts, settings, profile, metas, course, achievements, support

def main(page: ft.Page):
    page.title = "Finanzapp"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 850

    def route_change(route):
        page.views.clear()

        routes = {
            "/": login.view,
            "/dashboard": dashboard.view,
            "/expenses": expenses.view,
            "/charts": charts.view_charts,
            "/settings": settings.view,
            "/profile": profile.view,
            "/metas": metas.view_metas,
            "/course": course.view,
            "/achievements": achievements.view,
            "/support": support.view,
        }

        view_func = routes.get(page.route, login.view)
        page.views.append(view_func(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
