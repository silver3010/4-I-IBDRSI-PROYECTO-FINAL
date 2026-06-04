from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.alumno import Alumno
from app.models.grupo import Grupo
from app.models.calificacion import Calificacion
from functools import wraps

bp = Blueprint('alumnos', __name__, url_prefix='/alumnos')

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
    """Listar todos los alumnos"""
    grupo_id = request.args.get('grupo_id', None)
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Alumno.query
    
    if grupo_id:
        query = query.filter_by(grupo_id=grupo_id)
    
    alumnos_pagina = query.paginate(page=pagina, per_page=20)
    grupos = Grupo.query.filter_by(activo=True).all()
    
    return render_template('alumnos/listar.html',
                         alumnos_pagina=alumnos_pagina,
                         grupos=grupos,
                         grupo_id_seleccionado=grupo_id)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nuevo alumno"""
    if request.method == 'GET':
        grupos = Grupo.query.filter_by(activo=True).all()
        return render_template('alumnos/crear.html', grupos=grupos)
    
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        grupo_id = request.form.get('grupo_id', type=int)
        
        # Validaciones
        if not all([matricula, nombre, apellido]):
            return render_template('alumnos/crear.html', error='Todos los campos son requeridos'), 400
        
        if Alumno.query.filter_by(matricula=matricula).first():
            return render_template('alumnos/crear.html', error='La matrícula ya existe'), 409
        
        alumno = Alumno(
            matricula=matricula,
            nombre=nombre,
            apellido=apellido,
            grupo_id=grupo_id,
            activo=True
        )
        
        db.session.add(alumno)
        db.session.commit()
        
        return redirect(url_for('alumnos.listar')), 201

@bp.route('/<int:alumno_id>', methods=['GET'])
@login_required
def detalle(alumno_id):
    """Ver detalle de un alumno"""
    alumno = Alumno.query.get_or_404(alumno_id)
    calificaciones = Calificacion.query.filter_by(alumno_id=alumno_id).all()
    
    return render_template('alumnos/detalle.html',
                         alumno=alumno,
                         calificaciones=calificaciones)

@bp.route('/<int:alumno_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(alumno_id):
    """Editar alumno"""
    alumno = Alumno.query.get_or_404(alumno_id)
    grupos = Grupo.query.filter_by(activo=True).all()
    
    if request.method == 'GET':
        return render_template('alumnos/editar.html',
                             alumno=alumno,
                             grupos=grupos)
    
    if request.method == 'POST':
        alumno.nombre = request.form.get('nombre', alumno.nombre)
        alumno.apellido = request.form.get('apellido', alumno.apellido)
        alumno.grupo_id = request.form.get('grupo_id', alumno.grupo_id, type=int)
        
        db.session.commit()
        return redirect(url_for('alumnos.detalle', alumno_id=alumno.id)), 200

@bp.route('/<int:alumno_id>/eliminar', methods=['POST'])
@login_required
def eliminar(alumno_id):
    """Eliminar alumno"""
    alumno = Alumno.query.get_or_404(alumno_id)
    db.session.delete(alumno)
    db.session.commit()
    
    return redirect(url_for('alumnos.listar')), 200

@bp.route('/api/listar', methods=['GET'])
def api_listar():
    """API para listar alumnos en JSON"""
    grupo_id = request.args.get('grupo_id', None)
    
    query = Alumno.query
    if grupo_id:
        query = query.filter_by(grupo_id=grupo_id)
    
    alumnos = query.all()
    return jsonify([alumno.to_dict() for alumno in alumnos])
