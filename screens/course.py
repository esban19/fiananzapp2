import flet as ft
import json
import os
from utils.auth import get_user_by_id
# Simular ID de usuario activo (esto normalmente viene de login)


# Ruta del progreso
PROGRESO_PATH = "progreso.json"

# Contenido de los niveles
niveles_contenido = {
    1: {
        "titulo": "Introducción a las Finanzas",
    "introduccion": "¿Qué son las finanzas? Tipos, principios básicos, y su importancia.",
    "desarrollo": "La administración del dinero y otros activos. Tipos: Personales: manejo del dinero individual o familiar, Corporativas: gestión financiera de empresas, Públicas: finanzas del gobierno. Principios: ingreso, gasto, ahorro, inversión. Importancia: permite tomar decisiones informadas y alcanzar metas.",
    "quizz": {
      "pregunta": "¿Cuál de los siguientes es un principio básico de las finanzas?",
      "opciones": ["Ingreso", "Comprar ropa", "Viajar sin planificar"],
      "respuesta_correcta": "Ingreso"
        }
    },
    2: {
        "titulo": "Presupuesto Personal",
    "introduccion": "¿Qué es un presupuesto, cómo se elabora y por qué es importante?",
    "desarrollo": "Es un plan de ingresos y gastos para controlar tu dinero. Pasos: registrar ingresos y gastos, clasificarlos, asignar montos y ajustar según necesidades. Herramientas: Excel, Fintonic, YNAB.",
    "quizz": {
      "pregunta": "¿Cuál es la función principal de un presupuesto?",
      "opciones": ["Gastar más", "Controlar ingresos y gastos", "Evitar pagar impuestos"],
      "respuesta_correcta": "Controlar ingresos y gastos"
        }
    },
    3:{
        "titulo": "Ahorro",
    "introduccion": "Diferencias con la inversión, técnicas y objetivos del ahorro.",
    "desarrollo": "El ahorro es dinero reservado con bajo riesgo y alta liquidez. Técnicas: regla 50/30/20, ahorro automático. Objetivos: fondo de emergencia, metas personales. Productos: cuentas de ahorro, depósitos a plazo.",
    "quizz": {
      "pregunta": "¿Cuál es una técnica común para fomentar el ahorro?",
      "opciones": ["Pedir préstamos", "Regla 50/30/20", "Gastar todo el ingreso"],
      "respuesta_correcta": "Regla 50/30/20"
        }
    },
    4:{
        "titulo": "Deudas y Crédito",
    "introduccion": "Tipos de deuda, uso responsable del crédito y cómo evitar el sobreendeudamiento.",
    "desarrollo": "Deuda buena: genera valor (como estudios). Deuda mala: consumo innecesario. Tarjetas de crédito deben usarse con responsabilidad. Evitar solo pagar el mínimo. Intereses se acumulan si no se paga a tiempo.",
    "quizz": {
      "pregunta": "¿Cuál es un ejemplo de deuda buena?",
      "opciones": ["Crédito educativo", "Compras impulsivas", "Viajes sin presupuesto"],
      "respuesta_correcta": "Crédito educativo"
        }
    },
    5:{
          "titulo": "Inversiones Básicas",
    "introduccion": "Qué es invertir, tipos de instrumentos y el equilibrio entre riesgo y rentabilidad.",
    "desarrollo": "Invertir es poner tu dinero a trabajar. Instrumentos: acciones, bonos, fondos. Mayor rentabilidad suele implicar mayor riesgo. Importancia de diversificar. Define tu perfil de inversor.",
    "quizz": {
      "pregunta": "¿Qué implica mayor rentabilidad en una inversión?",
      "opciones": ["Menor riesgo", "Mayor riesgo", "Ningún riesgo"],
      "respuesta_correcta": "Mayor riesgo"
        }
    },
    6:{
          "titulo": "Finanzas Bancarias",
    "introduccion": "Cómo funcionan los bancos, tipos de cuentas y servicios que ofrecen.",
    "desarrollo": "Los bancos intermedian entre ahorradores y prestatarios. Cuentas: corriente (uso diario), ahorro (intereses), plazo fijo (mayor rentabilidad). Servicios: tarjetas, préstamos, seguros. Leer condiciones para evitar comisiones.",
    "quizz": {
      "pregunta": "¿Cuál de las siguientes es una cuenta bancaria común?",
      "opciones": ["Cuenta corriente", "Cuenta mensual", "Cuenta anual fija"],
      "respuesta_correcta": "Cuenta corriente"
        }
    },
    7:{
        "titulo": "Impuestos Personales",
    "introduccion": "Conceptos básicos, declaración de impuestos y planificación fiscal.",
    "desarrollo": "Impuestos directos (renta) e indirectos (IVA). Declaración anual de ingresos. Puedes deducir educación, salud, etc. Planificar ayuda a pagar menos legalmente.",
    "quizz": {
      "pregunta": "¿Qué tipo de impuesto es el IVA?",
      "opciones": ["Directo", "Indirecto", "Nulo"],
      "respuesta_correcta": "Indirecto"
        }
    },
    8:{
        "titulo": "Finanzas para el Emprendedor",
    "introduccion": "Costos, punto de equilibrio, flujo de caja y fijación de precios.",
    "desarrollo": "Costos fijos no cambian con la producción; los variables sí. Punto de equilibrio: ingresos = costos. Flujo de caja: dinero que entra y sale. Fijar precios que cubran costos y den ganancia.",
    "quizz": {
      "pregunta": "¿Qué representa el punto de equilibrio en un negocio?",
      "opciones": ["Donde se gana mucho", "Donde se cubren los costos", "Donde hay pérdidas"],
      "respuesta_correcta": "Donde se cubren los costos"
        }
    },
    9:{
        "titulo": "Planificación Financiera a Largo Plazo",
    "introduccion": "Pensiones, inversiones a largo plazo, seguros y metas financieras.",
    "desarrollo": "Planificar jubilación desde joven. Invertir a largo plazo para el retiro o educación. Seguros protegen tu estabilidad. Metas: casa, viajes, universidad. Usa productos financieros adecuados.",
    "quizz": {
      "pregunta": "¿Qué herramienta protege tus finanzas ante imprevistos?",
      "opciones": ["Crédito", "Seguro", "Préstamo informal"],
      "respuesta_correcta": "Seguro"
        }
    },
    10:{
        "titulo": "Hábitos Financieros Saludables",
    "introduccion": "Decisiones inteligentes para una vida financiera estable.",
    "desarrollo": "Tener un presupuesto, ahorrar regularmente, invertir con criterio, evitar deudas innecesarias y revisar tus finanzas frecuentemente son hábitos clave para el éxito financiero.",
    "quizz": {
      "pregunta": "¿Cuál de los siguientes es un hábito financiero saludable?",
      "opciones": ["Gastar todo el ingreso", "Ahorrar regularmente", "Usar crédito sin control"],
      "respuesta_correcta": "Ahorrar regularmente"
        }
    },
    # Puedes agregar aquí los otros niveles siguiendo el mismo formato
}

# Cargar progreso del archivo
def cargar_progreso():
    if not os.path.exists(PROGRESO_PATH):
        return {}
    with open(PROGRESO_PATH, "r") as f:
        return json.load(f)

# Guardar progreso actualizado
def guardar_progreso(progreso):
    with open(PROGRESO_PATH, "w") as f:
        json.dump(progreso, f)

# Vista principal del curso
def view(page: ft.Page):
    user_id = page.session.get("user")
    progreso = cargar_progreso()
    completados = set(progreso.get(str(user_id), []))
    nivel_seleccionado = ft.Text("", size=16, italic=True)
    progreso_bar = ft.ProgressBar(value=len(completados) / 10, width=400, color="green")
    contenedor = ft.Column()

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

    def mostrar_quizz(nivel, quizz):
        pregunta = ft.Text(quizz["pregunta"])
        opciones = []
        resultado = ft.Text("")

        def validar_respuesta(e):
            seleccion = e.control.text
            if seleccion == quizz["respuesta_correcta"]:
                resultado.value = "✅ Correcto. Nivel completado."
                completados.add(nivel)
                progreso[str(user_id)] = list(completados)
                guardar_progreso(progreso)
                progreso_bar.value = len(completados) / 10
            else:
                resultado.value = "❌ Incorrecto. Inténtalo de nuevo."
            page.update()

        for opcion in quizz["opciones"]:
            opciones.append(
                ft.ElevatedButton(text=opcion, on_click=validar_respuesta)
            )

        contenedor.controls = [pregunta, *opciones, resultado]
        page.update()

    def mostrar_contenido_nivel(nivel):
        contenedor.controls.clear()
        if nivel not in completados and (nivel > 1 and (nivel - 1) not in completados):
            nivel_seleccionado.value = f"🔒 El Nivel {nivel} está bloqueado."
            contenedor.controls = [nivel_seleccionado]
            page.update()
            return

        contenido = niveles_contenido[nivel]
        seccion_index = 0

        def avanzar_seccion(e):
            nonlocal seccion_index
            seccion_index += 1
            if seccion_index == 1:
                nivel_seleccionado.value = f"📘 Desarrollo:{contenido['desarrollo']}"
                btn_avanzar.text = "Ir al Quiz"
            elif seccion_index == 2:
                mostrar_quizz(nivel, contenido["quizz"])
                return
            page.update()

        nivel_seleccionado.value = f"📘 Introducción:{contenido['introduccion']}"
        btn_avanzar = ft.ElevatedButton(text="Siguiente", on_click=avanzar_seccion)
        contenedor.controls = [nivel_seleccionado, btn_avanzar]
        page.update()

    def crear_nivel(nivel_numero):
        desbloqueado = nivel_numero == 1 or (nivel_numero - 1) in completados
        completado = nivel_numero in completados

        color = "#4CAF50" if completado else "#2196F3" if desbloqueado else "#B0BEC5"
        icono = "check_circle" if completado else "lock_open" if desbloqueado else "lock"

        return ft.Container(
            content=ft.ElevatedButton(
                icon=icono,
                text=f"Nivel {nivel_numero}: {niveles_contenido.get(nivel_numero, {}).get('titulo', 'Educación Financiera')}",
                on_click=lambda e: mostrar_contenido_nivel(nivel_numero),
                style=ft.ButtonStyle(bgcolor=color, color="white"),
            ),
            padding=5
        )

    def pantalla_curso():
        niveles = [crear_nivel(i) for i in niveles_contenido]
        progreso_bar.value = len(completados) / 10

        return ft.Column(
            controls=[
                progreso_bar,
                ft.Divider(),
                *niveles,
                contenedor
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    return ft.View(
        route="/course",
        drawer=drawer,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.AppBar(
                title=ft.Text("Finanzapp"),
                leading=ft.IconButton(icon="menu", on_click=open_drawer)
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=pantalla_curso(),
                            padding=20
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True
            )
        ]
    )


