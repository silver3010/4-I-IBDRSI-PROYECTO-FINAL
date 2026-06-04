from app import db
from datetime import datetime

class Docente(db.Model):
    __tablename__ = 'docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_empleado = db.Column(db.String(30), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    telefono = db.Column(db.String(20))
    especialidad = db.Column(db.String(150))
    activo = db.Column(db.Boolean, default=True)
    fecha_contratacion = db.Column(db.Date)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    planeaciones = db.relationship('Planeacion', backref='docente', lazy=True, cascade='all, delete-orphan')
    calificaciones = db.relationship('Calificacion', backref='docente', lazy=True)
    
    def __repr__(self):
        return f'<Docente {self.nombre} {self.apellido}>'
    
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_empleado': self.numero_empleado,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'especialidad': self.especialidad,
            'activo': self.activo,
            'nombre_completo': self.nombre_completo()
        }
