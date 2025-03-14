from flask import render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
import re

def validar_contraseña(password):
    """Valida que la contraseña cumpla con los requisitos mínimos."""
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", password)

def index():
    """Página de inicio"""
    return render_template("index.html")

def register():
    """Maneja el registro de usuarios (GET y POST)."""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("routes.register"))

        # Validar la contraseña
        if not validar_contraseña(password):
            flash("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.", "danger")
            return redirect(url_for("routes.register"))

        # Crear el nuevo usuario con rol "usuario"
        new_user = User(username=username, email=email, role="usuario")
        new_user.set_password(password)  # Guardar contraseña encriptada

        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado con éxito.", "success")
        return redirect(url_for("routes.iniciar_sesion"))

    return render_template("register.html")


def iniciar_sesion():
    """Maneja el inicio de sesión de los usuarios."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("routes.index"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")

def cerrar_sesion():
    session.pop('_flashes', None)  # Elimina mensajes flash previos
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("routes.iniciar_sesion"))

from flask import flash, redirect, url_for
from flask_login import current_user

@login_required
def lista_usuarios():
    """Muestra una tabla con los usuarios registrados solo si el usuario es administrador."""
    if not current_user.role == "admin":  # Verifica si el usuario NO es administrador
        flash("No tienes permiso para ver esta página.", "danger")
        return redirect(url_for("routes.index"))  # Redirige a otra página (ajusta según tu app)
    
    usuarios = User.query.all()  # Obtiene todos los usuarios de la base de datos
    return render_template("users.html", usuarios=usuarios)


def editar_usuario(id):
    """Permite actualizar los datos de un usuario desde AJAX."""
    usuario = User.query.get_or_404(id)  # Obtiene el usuario o lanza error 404
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")  # Opcional

    # Validar si el correo ya está en uso por otro usuario
    usuario_existente = User.query.filter(User.email == email, User.id != id).first()
    if usuario_existente:
        return jsonify({"error": "Este correo ya está en uso por otro usuario"}), 400

    usuario.username = username
    usuario.email = email

    # Solo actualizar la contraseña si se ingresó una nueva
    if password:
        if not validar_contraseña(password):
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número."}), 400
        usuario.set_password(password)

    db.session.commit()
    return jsonify({"message": "Usuario actualizado con éxito"}), 200

@login_required
def eliminar_usuario(id):
    """Elimina un usuario desde AJAX con permisos adecuados."""
    usuario = User.query.get_or_404(id)

    # Si el usuario actual es admin, puede eliminar cualquier usuario
    if current_user.role == "admin":
        db.session.delete(usuario)
        db.session.commit()

        # Si el admin se elimina a sí mismo, cerrar su sesión
        if current_user.id == id:
            logout_user()
            session.clear()
            flash("Tu cuenta ha sido eliminada. Sesión cerrada.", "warning")
            return jsonify({"message": "Tu cuenta ha sido eliminada. Sesión cerrada."}), 200

        flash(f"El usuario {usuario.username} ha sido eliminado.", "success")
        return jsonify({"message": f"El usuario {usuario.username} ha sido eliminado."}), 200

    # Si el usuario NO es admin, solo puede eliminarse a sí mismo
    elif current_user.id == id:
        db.session.delete(usuario)
        db.session.commit()
        logout_user()
        session.clear()
        flash("Tu cuenta ha sido eliminada. Sesión cerrada.", "warning")
        return jsonify({"message": "Tu cuenta ha sido eliminada. Sesión cerrada."}), 200

    # Si no es admin y quiere eliminar a otro, se le niega el permiso
    else:
        flash("No tienes permisos para eliminar este usuario.", "danger")
        return jsonify({"error": "No tienes permisos para eliminar este usuario."}), 403  
