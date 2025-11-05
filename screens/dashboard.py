import flet as ft
import os
import json
from datetime import datetime

DATA_PATH = "data.json"

def cargar_datos():
    if not os.path.exists(DATA_PATH):
        return {"total_gastos": 0, "total_ingresos": 0, "total_ahorros": 0, "movimientos": []}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def view(page: ft.Page):
    data = cargar_datos()

    # Menú lateral
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

    # Gráfico circular
    pie_chart = ft.PieChart(
        sections=[],
        width=250,
        height=250
    )

    total_text = ft.Text(size=22, weight="bold")

    # Tabla de movimientos
    tabla_movimientos = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Fecha")),
            ft.DataColumn(label=ft.Text("Tipo")),
            ft.DataColumn(label=ft.Text("Categoría")),
            ft.DataColumn(label=ft.Text("Monto")),
        ],
        rows=[]
    )

    # Función para actualizar la vista con datos actuales
    def actualizar_vista():
        pie_chart.sections = [
            ft.PieChartSection(value=data["total_gastos"], title="Gastos", color="red"),
            ft.PieChartSection(value=data["total_ingresos"], title="Ingresos", color="green"),
            ft.PieChartSection(value=data["total_ahorros"], title="Ahorros", color="blue"),
        ]
        total_text.value = f"Total: ${data['total_ingresos'] - data['total_gastos']:.2f}"
        tabla_movimientos.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(mov["fecha"])),
                    ft.DataCell(ft.Text("Ingreso" if mov["tipo"] == "ingreso" else "Gasto")),
                    ft.DataCell(ft.Text(mov["categoria"])),
                    ft.DataCell(ft.Text(f"${mov['monto']:.2f}"))
                ]
            ) for mov in reversed(data["movimientos"])
        ]
        page.update()

    # Función para agregar ingreso o gasto usando BottomSheet
    def agregar_monto(tipo):
        categorias = {
            "gasto": ["Coche", "Ropa", "Comida", "Otros"],
            "ingreso": ["Pagos", "Abonos", "Transferencias", "Otros"]
        }

        campo_monto = ft.TextField(
            label="Monto", 
            keyboard_type="number",
            autofocus=True,
            prefix_text="$",
            width=200
        )
        
        dropdown_categoria = ft.Dropdown(
            label="Categoría",
            options=[ft.dropdown.Option(cat) for cat in categorias[tipo]],
            value=categorias[tipo][0],
            width=200
        )
        
        # Contenedor para el formulario
        form_container = ft.Container(
            content=ft.Column([
                ft.Text(f"Agregar {'Gasto' if tipo == 'gasto' else 'Ingreso'}", 
                        size=20, weight="bold"),
                ft.Row([campo_monto, dropdown_categoria], 
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton("Cancelar", on_click=lambda e: close_bottom_sheet()),
                    ft.ElevatedButton("Aceptar", on_click=lambda e: submit_form(tipo))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
        
        # Crear el BottomSheet
        bottom_sheet = ft.BottomSheet(
            content=form_container,
            open=True,
            on_dismiss=lambda e: print("Bottom sheet dismissed"),
            bgcolor="white",
            elevation=20,
            shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(10, 10, 0, 0))
        )
        
        page.overlay.append(bottom_sheet)
        page.update()
        
        # Función para cerrar el BottomSheet
        def close_bottom_sheet():
            page.overlay.remove(bottom_sheet)
            page.update()
        
        # Función para enviar el formulario
        def submit_form(tipo):
            try:
                monto = float(campo_monto.value)
                if monto <= 0:
                    raise ValueError("Monto debe ser mayor que cero")
                categoria = dropdown_categoria.value or "Otros"

                if tipo == "gasto":
                    data["total_gastos"] += monto
                else:
                    data["total_ingresos"] += monto

                data["movimientos"].append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "tipo": tipo,
                    "categoria": categoria,
                    "monto": monto
                })

                guardar_datos(data)
                actualizar_vista()
                close_bottom_sheet()
            except ValueError as err:
                campo_monto.error_text = str(err)
                campo_monto.update()

    actualizar_vista()

    return ft.View(
        route="/dashboard",
        drawer=drawer,
        controls=[
            ft.AppBar(
                title=ft.Text("Finanzapp"),
                leading=ft.IconButton(icon="menu", on_click=open_drawer)
            ),
            ft.Column([
                total_text,
                ft.Row([
                    ft.ElevatedButton("Agregar Gasto", 
                                     on_click=lambda e: agregar_monto("gasto"),
                                     icon="remove_circle"),
                    ft.ElevatedButton("Agregar Ingreso", 
                                     on_click=lambda e: agregar_monto("ingreso"),
                                     icon="add_circle")
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Resumen", size=18, weight="bold"),
                            pie_chart
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        width=350,
                        bgcolor="white",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=12, color="blue", offset=ft.Offset(0, 4))
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Historial de Movimientos", size=18, weight="bold"),
                            ft.Column(
                                controls=[tabla_movimientos],
                                height=200,
                                scroll=ft.ScrollMode.ALWAYS
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        bgcolor="white",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=12, color="blue", offset=ft.Offset(0, 4))
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30)
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO)
        ]
    )
