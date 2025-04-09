from fastapi import FastAPI, HTTPException
from models import Base, Personaje, Mision
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TDA_Cola import ArrayQueue
from Exceptions import OwnEmpty
import json  


# Crear una instancia de FastAPI
app = FastAPI()

# Configuración de la BD
engine = create_engine('sqlite:///rpg.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.post("/personajes/")
def crear_personaje(nombre: str):
    db = Session()
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    return {"id": personaje.id}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int):
    db = Session()
    personaje = db.get(Personaje, personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    queue = personaje.get_misiones_queue()
    misiones = db.query(Mision).filter(Mision.id.in_(json.loads(queue.to_json()))).all()
    return {"misiones": [{"id": m.id, "nombre": m.nombre} for m in misiones]}

@app.post("/misiones/")
def crear_mision(nombre: str, descripcion: str, experiencia: int):
    db = Session()
    mision = Mision(nombre=nombre, descripcion=descripcion, experiencia=experiencia)
    db.add(mision)
    db.commit()
    return {"id": mision.id}



@app.post("/personajes/{personaje_id}/misiones/")
def aceptar_mision(personaje_id: int, mision_id: int):
    db = Session()
    personaje = db.get(Personaje, personaje_id)
    mision = db.get(Mision, mision_id)
    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrados")
    
    queue = personaje.get_misiones_queue()  # Primero obtén la cola
    if mision.id in json.loads(queue.to_json()):  # Luego verifica
        raise HTTPException(status_code=400, detail="Misión ya aceptada")
    
    queue.enqueue(mision.id)
    personaje.set_misiones_queue(queue)
    db.commit()
    return {"message": "Misión aceptada"}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int):
    db = Session()
    personaje = db.get(Personaje, personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    
    queue = personaje.get_misiones_queue()
    try:
        mision_id = queue.dequeue()
        mision = db.get(Mision, mision_id)
        mision.estado = 'completada'
        personaje.experiencia_total += mision.experiencia
        personaje.set_misiones_queue(queue)
        db.commit()
        return {"mision_completada": mision.nombre}
    except OwnEmpty:
        raise HTTPException(status_code=400, detail="El personaje no tiene misiones pendientes")