from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from TDA_Cola import ArrayQueue
Base = declarative_base()

class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text)
    experiencia = Column(Integer, default=0)
    estado = Column(Enum('pendiente', 'completada', name='estados'), default='pendiente')
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    misiones_json = Column(String(1000))  # Almacena la cola de misiones como JSON
    experiencia_total = Column(Integer, default=0)

    def get_misiones_queue(self):
        """Convierte el JSON almacenado en una instancia de ArrayQueue."""
        if not self.misiones_json:
            return ArrayQueue()
        return ArrayQueue.from_json(self.misiones_json)

    def set_misiones_queue(self, queue):
        """Actualiza el JSON de misiones desde una ArrayQueue."""
        self.misiones_json = queue.to_json()