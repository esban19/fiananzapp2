import flet as ft
from utils.auth import authenticate, register_user, get_user

def view(page: ft.Page):
    # Campos de inicio de sesión
    email = ft.TextField(label="Correo", width=300, autofocus=True)
    password = ft.TextField(label="Contraseña", password=True, 
                           can_reveal_password=True, width=300)
    
    # Campos de registro
    registro_nombre = ft.TextField(label="Nombre completo", width=300)
    registro_email = ft.TextField(label="Correo", width=300)
    registro_password = ft.TextField(label="Contraseña", password=True, 
                                   can_reveal_password=True, width=300)
    registro_confirm_password = ft.TextField(label="Confirmar contraseña", 
                                           password=True, can_reveal_password=True, 
                                           width=300)
    
    # Contenedor de mensajes
    mensaje = ft.Text("", size=14)
    
    # Control de pestañas
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Iniciar sesión"),
            ft.Tab(text="Registrarse"),
        ],
        expand=1,
    )
    
    # Contenedores para los formularios
    login_form = ft.Column([
        ft.Text("Iniciar sesión", size=20, weight="bold"),
        email,
        password,
        mensaje,
        ft.ElevatedButton("Iniciar sesión", on_click=lambda e: login_handler(e))
    ], spacing=15, visible=True)
    
    register_form = ft.Column([
        ft.Text("Registrarse", size=20, weight="bold"),
        registro_nombre,
        registro_email,
        registro_password,
        registro_confirm_password,
        mensaje,
        ft.ElevatedButton("Registrarse", on_click=lambda e: register_handler(e))
    ], spacing=15, visible=False)
    
    # Contenedor principal
    content_container = ft.Container(
        content=ft.Column([login_form, register_form]),
        padding=20
    )
    
    def login_handler(e):
        if authenticate(email.value, password.value):
            user = get_user(email.value)
            page.session.set("user", user)
            page.go("/dashboard")
        else:
            mensaje.value = "Credenciales incorrectas"
            mensaje.color = "red"
            mensaje.update()

    def register_handler(e):
        nombre_val = registro_nombre.value.strip()
        email_val = registro_email.value.strip()
        password_val = registro_password.value
        confirm_val = registro_confirm_password.value
        
        # Validaciones
        if not all([nombre_val, email_val, password_val, confirm_val]):
            mensaje.value = "Por favor complete todos los campos"
            mensaje.color = "red"
            mensaje.update()
            return
            
        if password_val != confirm_val:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "red"
            mensaje.update()
            return
            
        if len(password_val) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje.color = "red"
            mensaje.update()
            return
            
        if register_user(nombre_val, email_val, password_val):
            mensaje.value = "¡Registro exitoso! Ahora puede iniciar sesión"
            mensaje.color = "green"
            mensaje.update()
            
            # Limpiar campos
            registro_nombre.value = ""
            registro_email.value = ""
            registro_password.value = ""
            registro_confirm_password.value = ""
            
            # Cambiar a pestaña de login
            tabs.selected_index = 0
            tab_changed(None)
        else:
            mensaje.value = "Este correo ya está registrado"
            mensaje.color = "red"
            mensaje.update()

    def tab_changed(e):
        mensaje.value = ""
        mensaje.color = "red"
        
        if tabs.selected_index == 0:  # Login
            login_form.visible = True
            register_form.visible = False
            # Solo enfocar si el campo está visible
            if login_form.visible:
                email.focus()
        else:  # Registro
            login_form.visible = False
            register_form.visible = True
            # Solo enfocar si el campo está visible
            if register_form.visible:
                registro_nombre.focus()
        
        content_container.update()

    tabs.on_change = tab_changed

    return ft.View(
        route="/",
        controls=[
            ft.Column([
                ft.Text("Finanzapp", size=30, weight="bold"),
                tabs,
                content_container
            ], 
            alignment=ft.MainAxisAlignment.CENTER, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )