import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

conn = sqlite3.connect("contactos.db")

class Contacto:
    def __init__(self, email, nombre, telefono):
        self.email = email
        self.nombre = nombre
        self.telefono = telefono

@app.route('/')
def root():
    return jsonify({"message": "API de contactos con SQLite"})

@app.route('/contactos', methods=['POST'])
def crear_contacto():
    data = request.json
    contacto = Contacto(data['email'], data['nombre'], data['telefono'])
    connection = conn.cursor()
    connection.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
                      (contacto.email, contacto.nombre, contacto.telefono))
    conn.commit()
    return jsonify(data)

@app.route('/contactos', methods=['GET'])
def obtener_contactos():
    connection = conn.cursor()
    connection.execute('SELECT * FROM contactos')
    contactos = [Contacto(email=row[0], nombre=row[1], telefono=row[2]) for row in connection]
    return jsonify([contacto.__dict__ for contacto in contactos])

@app.route('/contactos/<email>', methods=['GET'])
def obtener_contacto(email):
    connection = conn.cursor()
    connection.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    row = connection.fetchone()
    if row:
        contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
        return jsonify(contacto.__dict__)
    else:
        return jsonify({"message": "Contacto no encontrado"})

@app.route('/contactos/<email>', methods=['PUT'])
def actualizar_contacto(email):
    data = request.json
    connection = conn.cursor()
    connection.execute('UPDATE contactos SET nombre = ?, telefono = ? WHERE email = ?',
                      (data['nombre'], data['telefono'], email))
    conn.commit()
    return jsonify(data)

@app.route('/contactos/<email>', methods=['DELETE'])
def eliminar_contacto(email):
    connection = conn.cursor()
    connection.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return jsonify({"message": "Contacto eliminado"})

@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    return render_template('prueba.html')

if __name__ == "__main__":
    app.run()
