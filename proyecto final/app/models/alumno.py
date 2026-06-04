from app import db
from datetime import datetime

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='alumno', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Alumno {self.matricula}>'
    
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    def promedio(self):
        """Calcula el promedio de calificaciones"""
        if not self.calificaciones:
            return 0
        suma = sum(c.valor for c in self.calificaciones)
        return round(suma / len(self.calificaciones), 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo(),
            'grupo_id': self.grupo_id,
            'grupo_nombre': self.grupo.nombre if self.grupo else None,
            'activo': self.activo,
            'promedio': self.promedio(),
            'cantidad_calificaciones': len(self.calificaciones)
        }
