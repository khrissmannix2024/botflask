from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from main.models import db, User

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

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado con éxito.", "success")
        return redirect(url_for("routes.register"))

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
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("routes.iniciar_sesion"))
