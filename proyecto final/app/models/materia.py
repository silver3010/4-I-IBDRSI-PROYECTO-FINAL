from app import db
from datetime import datetime

class Materia(db.Model):
    __tablename__ = 'materias'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    creditos = db.Column(db.Integer, default=0)
    horas_semana = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    planeaciones = db.relationship('Planeacion', backref='materia', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Materia {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'creditos': self.creditos,
            'horas_semana': self.horas_semana,
            'activo': self.activo
        }
