# Codigo hecho desde deepseek, solo testeos sin API
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Personaje, Mision
from TDA_Cola import ArrayQueue

# 1. Configuración inicial de la base de datos
engine = create_engine('sqlite:///rpg.db')  # Base de datos SQLite
Base.metadata.create_all(engine)  # Crea las tablas
Session = sessionmaker(bind=engine)
db = Session()

# 2. Crear datos de prueba (misiones y personajes)
def crear_datos_iniciales():
    # Misiones de ejemplo
    mision1 = Mision(
        nombre="Derrota 5 slimes",
        descripcion="Elimina 5 slimes en el bosque",
        experiencia=100
    )
    mision2 = Mision(
        nombre="Recoge 3 hierbas",
        descripcion="Encuentra hierbas medicinales",
        experiencia=50
    )
    db.add_all([mision1, mision2])
    db.commit()

    # Personaje de ejemplo
    personaje = Personaje(nombre="Aragorn")
    db.add(personaje)
    db.commit()

    print("Datos iniciales creados: 2 misiones y 1 personaje.")

# 3. Probar el TDA Cola con SQLAlchemy
def probar_cola_misiones():
    personaje = db.query(Personaje).first()
    mision1, mision2 = db.query(Mision).all()

    # Crear cola y añadir misiones
    queue = ArrayQueue()
    queue.enqueue(mision1.id)
    queue.enqueue(mision2.id)

    # Guardar cola en el personaje
    personaje.misiones_json = queue.to_json()
    db.commit()

    # Recuperar cola desde la BD
    queue_recuperada = ArrayQueue.from_json(personaje.misiones_json)
    print(f"Misión FIFO: {queue_recuperada.dequeue()}")  # Debería ser la misión 1

# 4. Ejecutar pruebas
if __name__ == "__main__":
    crear_datos_iniciales()
    probar_cola_misiones()