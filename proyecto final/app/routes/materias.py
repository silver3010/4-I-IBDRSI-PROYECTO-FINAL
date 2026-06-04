from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.materia import Materia
from functools import wraps

bp = Blueprint('materias', __name__, url_prefix='/materias')

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
    """Listar todas las materias"""
    pagina = request.args.get('pagina', 1, type=int)
    
    materias_pagina = Materia.query.paginate(page=pagina, per_page=20)
    
    return render_template('materias/listar.html',
                         materias_pagina=materias_pagina)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nueva materia"""
    if request.method == 'GET':
        return render_template('materias/crear.html')
    
    if request.method == 'POST':
        clave = request.form.get('clave')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        creditos = request.form.get('creditos', 0, type=int)
        horas_semana = request.form.get('horas_semana', 0, type=int)
        
        if not all([clave, nombre]):
            return render_template('materias/crear.html', error='Clave y nombre son requeridos'), 400
        
        if Materia.query.filter_by(clave=clave).first():
            return render_template('materias/crear.html', error='La clave ya existe'), 409
        
        materia = Materia(
            clave=clave,
            nombre=nombre,
            descripcion=descripcion,
            creditos=creditos,
            horas_semana=horas_semana,
            activo=True
        )
        
        db.session.add(materia)
        db.session.commit()
        
        return redirect(url_for('materias.listar')), 201

@bp.route('/<int:materia_id>', methods=['GET'])
@login_required
def detalle(materia_id):
    """Ver detalle de una materia"""
    materia = Materia.query.get_or_404(materia_id)
    
    return render_template('materias/detalle.html',
                         materia=materia)

@bp.route('/<int:materia_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(materia_id):
    """Editar materia"""
    materia = Materia.query.get_or_404(materia_id)
    
    if request.method == 'GET':
        return render_template('materias/editar.html',
                             materia=materia)
    
    if request.method == 'POST':
        materia.nombre = request.form.get('nombre', materia.nombre)
        materia.descripcion = request.form.get('descripcion', materia.descripcion)
        materia.creditos = request.form.get('creditos', materia.creditos, type=int)
        materia.horas_semana = request.form.get('horas_semana', materia.horas_semana, type=int)
        
        db.session.commit()
        return redirect(url_for('materias.detalle', materia_id=materia.id)), 200

@bp.route('/<int:materia_id>/eliminar', methods=['POST'])
@login_required
def eliminar(materia_id):
    """Eliminar materia"""
    materia = Materia.query.get_or_404(materia_id)
    db.session.delete(materia)
    db.session.commit()
    
    return redirect(url_for('materias.listar')), 200

@bp.route('/api/listar', methods=['GET'])
def api_listar():
    """API para listar materias en JSON"""
    materias = Materia.query.filter_by(activo=True).all()
    return jsonify([materia.to_dict() for materia in materias])
