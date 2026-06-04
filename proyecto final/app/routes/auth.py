from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.usuario import Usuario
from datetime import datetime
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de login"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('auth/login.html', error='Email y contraseña son requeridos'), 400
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password) and usuario.activo:
            session['usuario_id'] = usuario.id
            session['usuario_email'] = usuario.email
            session['usuario_rol'] = usuario.rol
            session['usuario_nombre'] = usuario.nombre
            
            # Actualizar último login
            usuario.ultimo_login = datetime.utcnow()
            db.session.commit()
            
            return redirect(url_for('dashboard.index'))
        else:
            return render_template('auth/login.html', error='Email o contraseña incorrectos'), 401

@bp.route('/logout')
def logout():
    """Ruta de logout"""
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta de registro (solo para admin)"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        rol = request.form.get('rol', 'control_escolar')
        
        # Validaciones
        if not all([nombre, apellido, email, password]):
            return render_template('auth/register.html', error='Todos los campos son requeridos'), 400
        
        if password != password_confirm:
            return render_template('auth/register.html', error='Las contraseñas no coinciden'), 400
        
        if Usuario.query.filter_by(email=email).first():
            return render_template('auth/register.html', error='El email ya está registrado'), 409
        
        # Crear nuevo usuario
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            rol=rol,
            activo=True
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        return redirect(url_for('auth.login')), 201
