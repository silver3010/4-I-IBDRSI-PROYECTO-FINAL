from datetime import datetime
from functools import wraps

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from app import db
from app.models.docente import Docente
from app.models.grupo import Grupo
from app.models.materia import Materia
from app.models.planeacion import Planeacion

bp = Blueprint('planeacion', __name__, url_prefix='/planeacion')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def _catalogos():
    return {
        'grupos': Grupo.query.filter_by(activo=True).all(),
        'materias': Materia.query.filter_by(activo=True).all(),
        'docentes': Docente.query.filter_by(activo=True).all(),
        'dias_semana': ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
    }


@bp.route('/', methods=['GET'])
@login_required
def listar():
    grupo_id = request.args.get('grupo_id', type=int)
    materia_id = request.args.get('materia_id', type=int)
    docente_id = request.args.get('docente_id', type=int)
    pagina = request.args.get('pagina', 1, type=int)

    query = Planeacion.query
    if grupo_id:
        query = query.filter_by(grupo_id=grupo_id)
    if materia_id:
        query = query.filter_by(materia_id=materia_id)
    if docente_id:
        query = query.filter_by(docente_id=docente_id)

    planeaciones_pagina = query.order_by(Planeacion.dia_semana, Planeacion.hora_inicio).paginate(
        page=pagina,
        per_page=20,
    )

    return render_template(
        'planeacion/listar.html',
        planeaciones_pagina=planeaciones_pagina,
        grupo_id_seleccionado=grupo_id,
        materia_id_seleccionada=materia_id,
        docente_id_seleccionado=docente_id,
        **_catalogos(),
    )


@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    catalogos = _catalogos()

    if request.method == 'GET':
        return render_template('planeacion/crear.html', **catalogos)

    grupo_id = request.form.get('grupo_id', type=int)
    materia_id = request.form.get('materia_id', type=int)
    docente_id = request.form.get('docente_id', type=int)
    dia_semana = request.form.get('dia_semana')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    if not all([grupo_id, materia_id, docente_id, dia_semana, hora_inicio, hora_fin]):
        return render_template('planeacion/crear.html', error='Todos los campos marcados son requeridos', **catalogos), 400

    if hora_inicio >= hora_fin:
        return render_template('planeacion/crear.html', error='La hora de inicio debe ser menor que la hora de fin', **catalogos), 400

    planeacion = Planeacion(
        grupo_id=grupo_id,
        materia_id=materia_id,
        docente_id=docente_id,
        dia_semana=dia_semana,
        hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
        hora_fin=datetime.strptime(hora_fin, '%H:%M').time(),
        aula=request.form.get('aula'),
        periodo_escolar=request.form.get('periodo_escolar'),
        observaciones=request.form.get('observaciones'),
    )

    db.session.add(planeacion)
    db.session.commit()

    return redirect(url_for('planeacion.listar')), 201


@bp.route('/<int:planeacion_id>', methods=['GET'])
@login_required
def detalle(planeacion_id):
    planeacion = Planeacion.query.get_or_404(planeacion_id)
    return render_template('planeacion/detalle.html', planeacion=planeacion)


@bp.route('/<int:planeacion_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(planeacion_id):
    planeacion = Planeacion.query.get_or_404(planeacion_id)
    catalogos = _catalogos()

    if request.method == 'GET':
        return render_template('planeacion/editar.html', planeacion=planeacion, **catalogos)

    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    if hora_inicio and hora_fin and hora_inicio >= hora_fin:
        return render_template(
            'planeacion/editar.html',
            planeacion=planeacion,
            error='La hora de inicio debe ser menor que la hora de fin',
            **catalogos,
        ), 400

    planeacion.grupo_id = request.form.get('grupo_id', planeacion.grupo_id, type=int)
    planeacion.materia_id = request.form.get('materia_id', planeacion.materia_id, type=int)
    planeacion.docente_id = request.form.get('docente_id', planeacion.docente_id, type=int)
    planeacion.dia_semana = request.form.get('dia_semana', planeacion.dia_semana)
    planeacion.hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time() if hora_inicio else planeacion.hora_inicio
    planeacion.hora_fin = datetime.strptime(hora_fin, '%H:%M').time() if hora_fin else planeacion.hora_fin
    planeacion.aula = request.form.get('aula', planeacion.aula)
    planeacion.periodo_escolar = request.form.get('periodo_escolar', planeacion.periodo_escolar)
    planeacion.observaciones = request.form.get('observaciones', planeacion.observaciones)

    db.session.commit()
    return redirect(url_for('planeacion.detalle', planeacion_id=planeacion.id)), 200


@bp.route('/<int:planeacion_id>/eliminar', methods=['POST'])
@login_required
def eliminar(planeacion_id):
    planeacion = Planeacion.query.get_or_404(planeacion_id)
    db.session.delete(planeacion)
    db.session.commit()
    return redirect(url_for('planeacion.listar')), 200


@bp.route('/api/listar', methods=['GET'])
def api_listar():
    planeaciones = Planeacion.query.all()
    return jsonify([planeacion.to_dict() for planeacion in planeaciones])
