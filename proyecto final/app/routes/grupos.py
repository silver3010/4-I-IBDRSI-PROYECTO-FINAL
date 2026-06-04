from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.grupo import Grupo
from app.models.turno import Turno
from app.models.alumno import Alumno
from functools import wraps

bp = Blueprint('grupos', __name__, url_prefix='/grupos')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/', methods=['GET'])
@login_required
def listar():
    """Listar todos los grupos"""
    semestre = request.args.get('semestre', None)
    turno_id = request.args.get('turno_id', None)
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Grupo.query
    
    if semestre:
        query = query.filter_by(semestre=semestre)
    if turno_id:
        query = query.filter_by(turno_id=turno_id)
    
    grupos_pagina = query.paginate(page=pagina, per_page=20)
    turnos = Turno.query.filter_by(activo=True).all()
    
    return render_template('grupos/listar.html',
                         grupos_pagina=grupos_pagina,
                         turnos=turnos,
                         semestre_seleccionado=semestre,
                         turno_id_seleccionado=turno_id)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nuevo grupo"""
    turnos = Turno.query.filter_by(activo=True).all()

    if request.method == 'GET':
        return render_template('grupos/crear.html', turnos=turnos)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        semestre = request.form.get('semestre', type=int)
        aula = request.form.get('aula')
        turno_id = request.form.get('turno_id', type=int)
        
        if not all([nombre, semestre, turno_id]):
            return render_template('grupos/crear.html', error='Campos requeridos', turnos=turnos), 400
        
        grupo = Grupo(
            nombre=nombre,
            semestre=semestre,
            aula=aula,
            turno_id=turno_id,
            activo=True
        )
        
        db.session.add(grupo)
        db.session.commit()
        
        return redirect(url_for('grupos.listar')), 201

@bp.route('/<int:grupo_id>', methods=['GET'])
@login_required
def detalle(grupo_id):
    """Ver detalle de un grupo"""
    grupo = Grupo.query.get_or_404(grupo_id)
    alumnos = Alumno.query.filter_by(grupo_id=grupo_id).all()
    
    return render_template('grupos/detalle.html',
                         grupo=grupo,
                         alumnos=alumnos)

@bp.route('/<int:grupo_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(grupo_id):
    """Editar grupo"""
    grupo = Grupo.query.get_or_404(grupo_id)
    turnos = Turno.query.filter_by(activo=True).all()
    
    if request.method == 'GET':
        return render_template('grupos/editar.html',
                             grupo=grupo,
                             turnos=turnos)
    
    if request.method == 'POST':
        grupo.nombre = request.form.get('nombre', grupo.nombre)
        grupo.semestre = request.form.get('semestre', grupo.semestre, type=int)
        grupo.aula = request.form.get('aula', grupo.aula)
        grupo.turno_id = request.form.get('turno_id', grupo.turno_id, type=int)
        
        db.session.commit()
        return redirect(url_for('grupos.detalle', grupo_id=grupo.id)), 200

@bp.route('/<int:grupo_id>/eliminar', methods=['POST'])
@login_required
def eliminar(grupo_id):
    """Eliminar grupo"""
    grupo = Grupo.query.get_or_404(grupo_id)
    db.session.delete(grupo)
    db.session.commit()
    
    return redirect(url_for('grupos.listar')), 200

@bp.route('/api/listar', methods=['GET'])
def api_listar():
    """API para listar grupos en JSON"""
    grupos = Grupo.query.filter_by(activo=True).all()
    return jsonify([grupo.to_dict() for grupo in grupos])
