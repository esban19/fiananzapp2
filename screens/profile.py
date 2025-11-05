import flet as ft
from utils.auth import update_user_name, update_user_password, get_user_by_id, delete_user
import datetime

def view(page: ft.Page):
    # Obtener usuario de la sesión
    user = page.session.get("user")
    if not user:
        page.go("/")
        return
    
    # Cargar datos actualizados del usuario
    user_data = get_user_by_id(user["id"])
    
    # Elementos de la interfaz
    user_name = ft.Text(value=user_data["name"], size=24, weight="bold")
    user_email = ft.Text(value=user_data["email"], size=18, color="#757575")  # GREY_600
    
    # Campos editables
    edit_name = ft.TextField(
        label="Nombre completo",
        value=user_data["name"],
        width=300,
        visible=False
    )
    
    current_password = ft.TextField(
        label="Contraseña actual",
        password=True,
        can_reveal_password=True,
        width=300,
        visible=False
    )
    
    new_password = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        visible=False
    )
    
    confirm_password = ft.TextField(
        label="Confirmar nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        visible=False
    )
    
    # Mensajes de estado
    message = ft.Text("", color="red", size=14)
    success_message = ft.Text("", color="green", size=14)
    
    # Estadísticas del usuario
    stats = ft.Column([
        ft.Text("Estadísticas", size=20, weight="bold"),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("25", size=28, weight="bold"),
                    ft.Text("Días consecutivos", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                width=120,
                bgcolor="#e3f2fd",  # BLUE_50
                border_radius=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("87%", size=28, weight="bold"),
                    ft.Text("Metas completadas", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                width=120,
                bgcolor="#e3f2fd",  # BLUE_50
                border_radius=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("15", size=28, weight="bold"),
                    ft.Text("Logros", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                width=120,
                bgcolor="#e3f2fd",  # BLUE_50
                border_radius=10
            )
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    ])
    
    # Funciones para manejar acciones
    def toggle_edit_name(e):
        edit_name.visible = not edit_name.visible
        user_name.visible = not user_name.visible
        btn_edit_name.text = "Guardar" if edit_name.visible else "Editar nombre"
        page.update()
    
    def save_name(e):
        new_name = edit_name.value.strip()
        if not new_name:
            message.value = "El nombre no puede estar vacío"
            message.update()
            return
        
        if update_user_name(user["id"], new_name):
            user_name.value = new_name
            user_data["name"] = new_name
            page.session.set("user", user_data)
            success_message.value = "¡Nombre actualizado con éxito!"
            success_message.update()
            toggle_edit_name(None)
        else:
            message.value = "Error al actualizar el nombre"
            message.update()
    
    def toggle_change_password(e):
        current_password.visible = not current_password.visible
        new_password.visible = not new_password.visible
        confirm_password.visible = not confirm_password.visible
        btn_change_password.text = "Guardar" if current_password.visible else "Cambiar contraseña"
        page.update()
    
    def save_password(e):
        current = current_password.value
        new = new_password.value
        confirm = confirm_password.value
        
        if not current or not new or not confirm:
            message.value = "Todos los campos son obligatorios"
            message.update()
            return
            
        if new != confirm:
            message.value = "Las nuevas contraseñas no coinciden"
            message.update()
            return
            
        if len(new) < 6:
            message.value = "La contraseña debe tener al menos 6 caracteres"
            message.update()
            return
            
        if update_user_password(user["id"], current, new):
            success_message.value = "¡Contraseña actualizada con éxito!"
            success_message.update()
            # Limpiar campos
            current_password.value = ""
            new_password.value = ""
            confirm_password.value = ""
            toggle_change_password(None)
        else:
            message.value = "Contraseña actual incorrecta"
            message.update()
    
    def logout(e):
        page.session.remove("user")
        page.go("/")
    
    def delete_account(e):
        def confirm_delete(e):
            if delete_user(user["id"]):
                dlg.open = False
                page.session.remove("user")
                page.go("/")
            else:
                message.value = "Error al eliminar la cuenta"
                message.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
                ft.TextButton("Eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color="red")),
            ],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    # Botones (usando nombres de iconos como strings)
    btn_edit_name = ft.ElevatedButton(
        "Editar nombre", 
        icon="edit",  # Nombre del icono como string
        on_click=toggle_edit_name
    )
    
    btn_save_name = ft.ElevatedButton(
        "Guardar", 
        icon="save",  # Nombre del icono como string
        on_click=save_name,
        visible=False
    )
    
    btn_change_password = ft.ElevatedButton(
        "Cambiar contraseña", 
        icon="vpn_key",  # Nombre del icono como string
        on_click=toggle_change_password
    )
    
    btn_save_password = ft.ElevatedButton(
        "Guardar contraseña", 
        icon="save",  # Nombre del icono como string
        on_click=save_password,
        visible=False
    )
    
    btn_logout = ft.ElevatedButton(
        "Cerrar sesión", 
        icon="exit_to_app",  # Nombre del icono como string
        on_click=logout,
        style=ft.ButtonStyle(color="blue")
    )
    
    btn_delete = ft.TextButton(
        "Eliminar cuenta",
        icon="delete",  # Nombre del icono como string
        on_click=delete_account,
        style=ft.ButtonStyle(color="red")
    )
    
    # Contenido principal
    content = ft.Column([
        ft.Row([
            ft.Icon("account_circle", size=80),  # Icono por nombre
            ft.Column([
                user_name,
                user_email,
                ft.Text(f"Miembro desde: {datetime.datetime.now().strftime('%d/%m/%Y')}", 
                        size=14, color="#9e9e9e")  # GREY_500
            ])
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Divider(),
        
        # Sección de edición de nombre
        ft.Column([
            ft.Text("Información personal", size=20, weight="bold"),
            edit_name,
            ft.Row([
                btn_edit_name,
                btn_save_name
            ], spacing=10)
        ], spacing=10),
        
        # Sección de cambio de contraseña
        ft.Column([
            ft.Text("Seguridad", size=20, weight="bold"),
            current_password,
            new_password,
            confirm_password,
            ft.Row([
                btn_change_password,
                btn_save_password
            ], spacing=10)
        ], spacing=10),
        
        # Mensajes
        message,
        success_message,
        
        ft.Divider(),
        
        # Estadísticas
        stats,
        
        ft.Divider(),
        
        # Acciones de cuenta
        ft.Column([
            ft.Text("Acciones de cuenta", size=20, weight="bold"),
            btn_logout,
            btn_delete
        ], spacing=15)
        
    ], spacing=20, scroll=ft.ScrollMode.AUTO)
    
    # Crear la vista sin el parámetro on_view_show
    return ft.View(
        route="/profile",
        controls=[
            ft.AppBar(title=ft.Text("Perfil")),
            ft.Container(
                content=content,
                padding=30,
                expand=True
            )
        ]
    )