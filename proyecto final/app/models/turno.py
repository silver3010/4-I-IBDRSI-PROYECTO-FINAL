from app import db
from datetime import datetime

class Turno(db.Model):
    __tablename__ = 'turnos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    grupos = db.relationship('Grupo', backref='turno', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Turno {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'hora_inicio': str(self.hora_inicio) if self.hora_inicio else None,
            'hora_fin': str(self.hora_fin) if self.hora_fin else None,
            'activo': self.activo
        }
