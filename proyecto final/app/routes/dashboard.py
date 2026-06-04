from flask import Blueprint, render_template, session, redirect, url_for
from app import db
from app.models.usuario import Usuario
from app.models.alumno import Alumno
from app.models.grupo import Grupo
from app.models.materia import Materia
from app.models.calificacion import Calificacion
from functools import wraps

bp = Blueprint('dashboard', __name__, url_prefix='/')

def login_required(f):
    """Decorador para requerir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir rol admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session or session.get('usuario_rol') != 'admin':
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
def index():
    """Dashboard principal"""
    # Obtener estadísticas
    total_alumnos = Alumno.query.count()
    total_grupos = Grupo.query.count()
    total_materias = Materia.query.count()
    total_calificaciones = Calificacion.query.count()
    
    # Promedios
    calificaciones = Calificacion.query.all()
    promedio_general = 0
    if calificaciones:
        promedio_general = round(sum(c.valor for c in calificaciones) / len(calificaciones), 2)
    
    # Estudiantes con bajo rendimiento
    alumnos_bajo_rendimiento = []
    for alumno in Alumno.query.all():
        if alumno.promedio() < 7:
            alumnos_bajo_rendimiento.append(alumno)
    
    return render_template('dashboard/index.html',
                         total_alumnos=total_alumnos,
                         total_grupos=total_grupos,
                         total_materias=total_materias,
                         total_calificaciones=total_calificaciones,
                         promedio_general=promedio_general,
                         alumnos_bajo_rendimiento=alumnos_bajo_rendimiento[:10])

@bp.route('/')
def home():
    """Ruta home, redirige a login o dashboard"""
    if 'usuario_id' in session:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))
