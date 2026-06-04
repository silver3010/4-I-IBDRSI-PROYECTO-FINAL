from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.docente import Docente
from functools import wraps

bp = Blueprint('docentes', __name__, url_prefix='/docentes')

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
    """Listar todos los docentes"""
    pagina = request.args.get('pagina', 1, type=int)
    
    docentes_pagina = Docente.query.paginate(page=pagina, per_page=20)
    
    return render_template('docentes/listar.html',
                         docentes_pagina=docentes_pagina)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nuevo docente"""
    if request.method == 'GET':
        return render_template('docentes/crear.html')
    
    if request.method == 'POST':
        numero_empleado = request.form.get('numero_empleado')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        especialidad = request.form.get('especialidad')
        
        if not all([numero_empleado, nombre, apellido]):
            return render_template('docentes/crear.html', error='Campos requeridos'), 400
        
        if Docente.query.filter_by(numero_empleado=numero_empleado).first():
            return render_template('docentes/crear.html', error='El número de empleado ya existe'), 409
        
        docente = Docente(
            numero_empleado=numero_empleado,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            especialidad=especialidad,
            activo=True
        )
        
        db.session.add(docente)
        db.session.commit()
        
        return redirect(url_for('docentes.listar')), 201

@bp.route('/<int:docente_id>', methods=['GET'])
@login_required
def detalle(docente_id):
    """Ver detalle de un docente"""
    docente = Docente.query.get_or_404(docente_id)
    
    return render_template('docentes/detalle.html',
                         docente=docente)

@bp.route('/<int:docente_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(docente_id):
    """Editar docente"""
    docente = Docente.query.get_or_404(docente_id)
    
    if request.method == 'GET':
        return render_template('docentes/editar.html',
                             docente=docente)
    
    if request.method == 'POST':
        docente.nombre = request.form.get('nombre', docente.nombre)
        docente.apellido = request.form.get('apellido', docente.apellido)
        docente.email = request.form.get('email', docente.email)
        docente.telefono = request.form.get('telefono', docente.telefono)
        docente.especialidad = request.form.get('especialidad', docente.especialidad)
        
        db.session.commit()
        return redirect(url_for('docentes.detalle', docente_id=docente.id)), 200

@bp.route('/<int:docente_id>/eliminar', methods=['POST'])
@login_required
def eliminar(docente_id):
    """Eliminar docente"""
    docente = Docente.query.get_or_404(docente_id)
    db.session.delete(docente)
    db.session.commit()
    
    return redirect(url_for('docentes.listar')), 200

@bp.route('/api/listar', methods=['GET'])
def api_listar():
    """API para listar docentes en JSON"""
    docentes = Docente.query.filter_by(activo=True).all()
    return jsonify([docente.to_dict() for docente in docentes])
