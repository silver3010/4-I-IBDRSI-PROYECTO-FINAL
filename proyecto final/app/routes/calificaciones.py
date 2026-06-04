from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.calificacion import Calificacion
from app.models.alumno import Alumno
from app.models.docente import Docente
from app.models.planeacion import Planeacion
from functools import wraps
from datetime import datetime

bp = Blueprint('calificaciones', __name__, url_prefix='/calificaciones')

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
    """Listar todas las calificaciones"""
    alumno_id = request.args.get('alumno_id', None)
    tipo = request.args.get('tipo', None)
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Calificacion.query
    
    if alumno_id:
        query = query.filter_by(alumno_id=alumno_id)
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    calificaciones_pagina = query.paginate(page=pagina, per_page=20)
    alumnos = Alumno.query.all()
    
    return render_template('calificaciones/listar.html',
                         calificaciones_pagina=calificaciones_pagina,
                         alumnos=alumnos,
                         alumno_id_seleccionado=alumno_id,
                         tipo_seleccionado=tipo)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nueva calificación"""
    if request.method == 'GET':
        alumnos = Alumno.query.all()
        docentes = Docente.query.all()
        planeaciones = Planeacion.query.all()
        tipos = ['Parcial', 'Final', 'Tarea', 'Participacion']
        return render_template('calificaciones/crear.html',
                             alumnos=alumnos,
                             docentes=docentes,
                             planeaciones=planeaciones,
                             tipos=tipos)
    
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id', type=int)
        valor = request.form.get('valor', type=float)
        tipo = request.form.get('tipo')
        docente_id = request.form.get('docente_id', type=int)
        planeacion_id = request.form.get('planeacion_id', type=int)
        comentarios = request.form.get('comentarios')
        fecha = request.form.get('fecha')
        
        if not all([alumno_id, valor, tipo]):
            return render_template('calificaciones/crear.html', error='Campos requeridos'), 400
        
        if valor < 0 or valor > 10:
            return render_template('calificaciones/crear.html', error='La calificación debe estar entre 0 y 10'), 400
        
        calificacion = Calificacion(
            alumno_id=alumno_id,
            valor=valor,
            tipo=tipo,
            docente_id=docente_id,
            planeacion_id=planeacion_id,
            comentarios=comentarios,
            fecha=datetime.strptime(fecha, '%Y-%m-%d').date() if fecha else None
        )
        
        db.session.add(calificacion)
        db.session.commit()
        
        return redirect(url_for('calificaciones.listar')), 201

@bp.route('/<int:calificacion_id>', methods=['GET'])
@login_required
def detalle(calificacion_id):
    """Ver detalle de una calificación"""
    calificacion = Calificacion.query.get_or_404(calificacion_id)
    
    return render_template('calificaciones/detalle.html',
                         calificacion=calificacion)

@bp.route('/<int:calificacion_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(calificacion_id):
    """Editar calificación"""
    calificacion = Calificacion.query.get_or_404(calificacion_id)
    alumnos = Alumno.query.all()
    docentes = Docente.query.all()
    tipos = ['Parcial', 'Final', 'Tarea', 'Participacion']
    
    if request.method == 'GET':
        return render_template('calificaciones/editar.html',
                             calificacion=calificacion,
                             alumnos=alumnos,
                             docentes=docentes,
                             tipos=tipos)
    
    if request.method == 'POST':
        valor = request.form.get('valor', type=float)
        
        if valor < 0 or valor > 10:
            return render_template('calificaciones/editar.html',
                                 error='La calificación debe estar entre 0 y 10',
                                 calificacion=calificacion), 400
        
        calificacion.valor = valor
        calificacion.tipo = request.form.get('tipo', calificacion.tipo)
        calificacion.comentarios = request.form.get('comentarios', calificacion.comentarios)
        fecha = request.form.get('fecha')
        if fecha:
            calificacion.fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        db.session.commit()
        return redirect(url_for('calificaciones.detalle', calificacion_id=calificacion.id)), 200

@bp.route('/<int:calificacion_id>/eliminar', methods=['POST'])
@login_required
def eliminar(calificacion_id):
    """Eliminar calificación"""
    calificacion = Calificacion.query.get_or_404(calificacion_id)
    db.session.delete(calificacion)
    db.session.commit()
    
    return redirect(url_for('calificaciones.listar')), 200

@bp.route('/api/listar', methods=['GET'])
def api_listar():
    """API para listar calificaciones en JSON"""
    alumno_id = request.args.get('alumno_id', None)
    
    query = Calificacion.query
    if alumno_id:
        query = query.filter_by(alumno_id=alumno_id)
    
    calificaciones = query.all()
    return jsonify([cal.to_dict() for cal in calificaciones])

@bp.route('/reportes/por-alumno', methods=['GET'])
@login_required
def reporte_por_alumno():
    """Reporte de calificaciones por alumno"""
    alumnos = Alumno.query.all()
    
    datos_alumnos = []
    for alumno in alumnos:
        datos_alumnos.append({
            'alumno': alumno,
            'promedio': alumno.promedio(),
            'cantidad_calificaciones': len(alumno.calificaciones),
            'estado': 'Aprobado' if alumno.promedio() >= 7 else 'Reprobado'
        })
    
    return render_template('calificaciones/reporte_alumnos.html',
                         datos_alumnos=datos_alumnos)

@bp.route('/reportes/por-grupo', methods=['GET'])
@login_required
def reporte_por_grupo():
    """Reporte de calificaciones por grupo"""
    from app.models.grupo import Grupo
    
    grupos = Grupo.query.all()
    datos_grupos = []
    
    for grupo in grupos:
        promedios = []
        for alumno in grupo.alumnos:
            if alumno.promedio() > 0:
                promedios.append(alumno.promedio())
        
        promedio_grupo = sum(promedios) / len(promedios) if promedios else 0
        
        datos_grupos.append({
            'grupo': grupo,
            'promedio_grupo': round(promedio_grupo, 2),
            'cantidad_alumnos': len(grupo.alumnos),
            'aprobados': len([a for a in grupo.alumnos if a.promedio() >= 7])
        })
    
    return render_template('calificaciones/reporte_grupos.html',
                         datos_grupos=datos_grupos)
