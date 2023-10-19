import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

conn = sqlite3.connect("contactos.db")

app = FastAPI()

class Contacto(BaseModel):
    email: str
    nombre: str
    telefono: str

@app.get('/')
def root():
    return {"message" : "API de contactos con SQLITE"}

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    connection = conn.cursor()
    connection.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
                      (contacto.email, contacto.nombre, contacto.telefono))
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    connection = conn.cursor()
    connection.execute('SELECT * FROM contactos')
    
    contactos = []
    for row in connection:
        contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
        contactos.append(contacto)
    
    return contactos

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    connection = conn.cursor()
    connection.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    
    for row in connection:
        contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
        return contacto
    
    return None

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    connection = conn.cursor()
    connection.execute('UPDATE contactos SET nombre = ?, telefono = ? WHERE email = ?',
                      (contacto.nombre, contacto.telefono, email))
    conn.commit()
    return contacto

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    connection = conn.cursor()
    connection.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return {"message": "Contacto eliminado"}
