from app import db
from datetime import datetime

class Grupo(db.Model):
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    aula = db.Column(db.String(50))
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    alumnos = db.relationship('Alumno', backref='grupo', lazy=True, cascade='all, delete-orphan')
    planeaciones = db.relationship('Planeacion', backref='grupo', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Grupo {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'semestre': self.semestre,
            'aula': self.aula,
            'turno_id': self.turno_id,
            'turno_nombre': self.turno.nombre if self.turno else None,
            'activo': self.activo,
            'cantidad_alumnos': len(self.alumnos)
        }
