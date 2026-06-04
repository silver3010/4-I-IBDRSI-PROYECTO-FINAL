from app import db
from datetime import datetime

class Planeacion(db.Model):
    __tablename__ = 'planeaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    aula = db.Column(db.String(50))
    periodo_escolar = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='planeacion', lazy=True)
    
    def __repr__(self):
        return f'<Planeacion {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'grupo_id': self.grupo_id,
            'grupo_nombre': self.grupo.nombre if self.grupo else None,
            'materia_id': self.materia_id,
            'materia_nombre': self.materia.nombre if self.materia else None,
            'docente_id': self.docente_id,
            'docente_nombre': self.docente.nombre_completo() if self.docente else None,
            'dia_semana': self.dia_semana,
            'hora_inicio': str(self.hora_inicio) if self.hora_inicio else None,
            'hora_fin': str(self.hora_fin) if self.hora_fin else None,
            'aula': self.aula,
            'periodo_escolar': self.periodo_escolar,
            'observaciones': self.observaciones
        }
