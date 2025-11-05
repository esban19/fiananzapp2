import flet as ft
import datetime
import os
import json

DATA_PATH = "data.json"

def build_drawer(page: ft.Page):
    return ft.NavigationDrawer(
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

def build_appbar(page: ft.Page, open_drawer_handler):
    return ft.AppBar(
        title=ft.Text("Finanzapp"),
        leading=ft.IconButton(icon="menu", on_click=open_drawer_handler)
    )

# ✅ FUNCIONES NUEVAS CON ID DE USUARIO
def cargar_metas(usuario_id="default"):
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data.get("metas_por_usuario", {}).get(usuario_id, [])

def guardar_metas(metas, usuario_id="default"):
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if "metas_por_usuario" not in data:
        data["metas_por_usuario"] = {}

    data["metas_por_usuario"][usuario_id] = metas

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ✅ VISTA MODIFICADA
def view_metas(page: ft.Page, usuario_id="default"):
    drawer = build_drawer(page)

    def open_drawer(e):
        drawer.open = True
        page.update()

    appbar = build_appbar(page, open_drawer)

    metas = cargar_metas(usuario_id)
    metas_column = ft.Column()

    def agregar_meta(e):
        nombre = nombre_input.value.strip()
        fecha_limite_str = fecha_input.value.strip()
        try:
            cantidad = float(cantidad_input.value)
        except:
            cantidad = None

        if not nombre or cantidad is None or cantidad <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("Datos inválidos. Verifica nombre y cantidad."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            fecha_limite = datetime.datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
            if fecha_limite < datetime.date.today():
                raise ValueError
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Fecha inválida (YYYY-MM-DD y no anterior a hoy)."))
            page.snack_bar.open = True
            page.update()
            return

        meta = {
            "nombre": nombre,
            "cantidad": cantidad,
            "progreso": 0.0,
            "fecha_limite": fecha_limite_str
        }
        metas.append(meta)
        guardar_metas(metas, usuario_id)
        actualizar_lista_metas()

        nombre_input.value = ""
        cantidad_input.value = ""
        fecha_input.value = ""
        page.update()

    def actualizar_lista_metas():
        metas_column.controls.clear()
        hoy = datetime.date.today()

        for i, meta in enumerate(metas):
            progreso_porcentaje = min(meta['progreso'] / meta['cantidad'], 1.0)

            progreso_input = ft.TextField(label="Monto ahorrado", width=200, keyboard_type=ft.KeyboardType.NUMBER)

            def agregar_progreso(e, m=meta, input_field=progreso_input):
                try:
                    cantidad = float(input_field.value)
                    if cantidad <= 0:
                        raise ValueError
                    m['progreso'] += cantidad
                    input_field.value = ""
                    guardar_metas(metas, usuario_id)
                    actualizar_lista_metas()
                except:
                    page.snack_bar = ft.SnackBar(ft.Text("Cantidad inválida."))
                    page.snack_bar.open = True
                    page.update()

            def eliminar_meta(e, index=i):
                metas.pop(index)
                guardar_metas(metas, usuario_id)
                actualizar_lista_metas()

            try:
                fecha_limite = datetime.datetime.strptime(meta["fecha_limite"], "%Y-%m-%d").date()
            except:
                fecha_limite = None

            vencida = fecha_limite and (fecha_limite < hoy)
            meta_completada = meta['progreso'] >= meta['cantidad']
            bgcolor = "#f8f9fa"
            if meta_completada:
                bgcolor = "#e6ffe6"
            elif vencida:
                bgcolor = "#ffe6e6"

            contenido_meta = [
                ft.Text(f"Meta: {meta['nombre']} - Total: ${meta['cantidad']:.2f}", size=16),
                ft.Text(f"Fecha límite: {fecha_limite.strftime('%Y-%m-%d') if fecha_limite else 'No definida'}",
                        size=14, color="red" if vencida else "black"),
                ft.ProgressBar(value=progreso_porcentaje, width=300, color="green"),
                ft.Text(f"Ahorrado: ${meta['progreso']:.2f} de ${meta['cantidad']:.2f}"),
            ]

            if meta_completada:
                contenido_meta.append(ft.Text("🎉 ¡Meta completada! 🎉", size=18, weight="bold", color="green"))
            elif vencida:
                contenido_meta.append(ft.Text("⚠️ Meta vencida", size=16, weight="bold", color="red"))
            else:
                contenido_meta.append(
                    ft.Row([progreso_input, ft.ElevatedButton("Agregar", on_click=agregar_progreso)])
                )

            contenido_meta.append(
                ft.TextButton("Eliminar", icon="delete", on_click=eliminar_meta, style=ft.ButtonStyle(color="red"))
            )

            metas_column.controls.append(
                ft.Container(
                    content=ft.Column(contenido_meta),
                    padding=10,
                    margin=ft.margin.only(bottom=10),
                    bgcolor=bgcolor,
                    border_radius=10,
                    animate=ft.Animation(400, "easeInOut")
                )
            )

        page.update()

    nombre_input = ft.TextField(label="Nombre de la meta", width=300)
    cantidad_input = ft.TextField(label="Cantidad total", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    fecha_input = ft.TextField(label="Fecha límite (YYYY-MM-DD)", width=300)
    agregar_btn = ft.ElevatedButton(text="Agregar Meta", on_click=agregar_meta)

    formulario = ft.Column(
        controls=[
            nombre_input,
            cantidad_input,
            fecha_input,
            agregar_btn,
            ft.Divider(),
            ft.Text("Tus Metas:", size=20, weight="bold"),
            metas_column
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    actualizar_lista_metas()

    return ft.View(
        route="/metas",
        drawer=drawer,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[
            appbar,
            ft.Container(content=formulario, padding=20, expand=True)
        ]
    )
