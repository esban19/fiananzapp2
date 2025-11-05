import flet as ft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
import json
from datetime import datetime
from data import get_totales

# Gráfico de barras
def generar_grafico_base64():
    total_gastos, total_ingresos, _ = get_totales()
    labels = ["Gastos", "Ingresos"]
    values = [total_gastos, total_ingresos]
    colors = ["#f44336", "#4caf50"]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(labels, values, color=colors)
    ax.set_ylabel("Monto")
    ax.set_title("Resumen de Gastos e Ingresos")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# Gráfico de dispersión
def generar_grafico_dispersion_base64():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    movimientos = data.get("movimientos", [])
    gastos = [m for m in movimientos if m["tipo"] == "gasto"]

    if not gastos:
        return None

    fechas = [datetime.strptime(m["fecha"], "%Y-%m-%d %H:%M") for m in gastos]
    montos = [m["monto"] for m in gastos]
    categorias = [m["categoria"] for m in gastos]

    # Colores distintos por categoría
    colores_categoria = {
        "Comida": "#e91e63",
        "Coche": "#2196f3",
        "Servicios": "#ff9800",
        "Otros": "#9c27b0"
    }
    colores = [colores_categoria.get(cat, "#607d8b") for cat in categorias]

    fig, ax = plt.subplots(figsize=(4, 3))
    scatter = ax.plot(fechas, montos, color="#607d8b", linewidth=2, label="Tendencia")
    ax.scatter(fechas, montos, c=colores, s=100, alpha=0.8, label="Gastos individuales")
    ax.legend()

    ax.set_title("Gastos en el Tiempo")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Monto")
    fig.autofmt_xdate()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# Vista charts
def view_charts(page: ft.Page):
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(ft.Text("Menú", size=20, weight="bold"), padding=10),
            ft.NavigationDrawerDestination(icon="person", label="Perfil"),
            ft.NavigationDrawerDestination(icon="home", label="Inicio"),
            ft.NavigationDrawerDestination(icon="flag", label="Metas"),
            ft.NavigationDrawerDestination(icon="pie_chart", label="Gráficos"),
            ft.NavigationDrawerDestination(icon="school", label="Curso"),
            ft.NavigationDrawerDestination(icon="star", label="Logros"),
            ft.NavigationDrawerDestination(icon="settings", label="Ajustes"),
            ft.NavigationDrawerDestination(icon="help", label="Soporte"),
        ],
        on_change=lambda e: page.go([
            "/profile", "/dashboard", "/metas", "/charts", "/course", "/achievements", "/settings", "/support"
        ][e.control.selected_index])
    )

    def open_drawer(e):
        drawer.open = True
        page.update()

    img_base64 = generar_grafico_base64()
    dispersion_base64 = generar_grafico_dispersion_base64()

    return ft.View(
        route="/charts",
        drawer=drawer,
        controls=[
            ft.AppBar(
                title=ft.Text("Gráficos"),
                leading=ft.IconButton(icon="menu", on_click=open_drawer),
            ),
            ft.Column(
                [
                    ft.Text("Resumen de Gastos e Ingresos", size=22, weight="bold"),
                    ft.Row(
                        [ft.Image(src_base64=img_base64, width=400, height=300)],
                         alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ft.Text("Gastos en el Tiempo", size=22, weight="bold"),
                    ft.Row(
                        [
                        ft.Image(src_base64=dispersion_base64, width=400, height=300)
                        if dispersion_base64
                        else ft.Text("No hay datos de gastos para mostrar.")
                        ],
                    alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            ),
        ],
    )
