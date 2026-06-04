from app import db
from datetime import datetime

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    planeacion_id = db.Column(db.Integer, db.ForeignKey('planeaciones.id'), nullable=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=True)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), default='Parcial')  # Parcial, Final, Tarea, Participacion
    fecha = db.Column(db.Date)
    comentarios = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Calificacion {self.id}>'
    
    def estado(self):
        """Retorna el estado de la calificación"""
        if self.valor >= 7:
            return 'Aprobado'
        else:
            return 'Reprobado'
    
    def to_dict(self):
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'alumno_nombre': self.alumno.nombre_completo() if self.alumno else None,
            'planeacion_id': self.planeacion_id,
            'docente_id': self.docente_id,
            'docente_nombre': self.docente.nombre_completo() if self.docente else None,
            'valor': self.valor,
            'tipo': self.tipo,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'comentarios': self.comentarios,
            'estado': self.estado()
        }
