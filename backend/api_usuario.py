from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app, origins='*')

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:oDSEzjdaim3MSgGjYbm1@database-1.cwsnkubwbttj.us-east-1.rds.amazonaws.com:3306/ipaw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)

# Modelos
class Usuario(db.Model):
    __tablename__ = 'usuario'
    dni = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    contrasenia = db.Column(db.String(60), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.nombre

    def serialize(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "contrasenia": self.contrasenia,
            "direccion": self.direccion
        }

# Rutas
@app.route('/usuarios', methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    usuarios_serialize = [usuario.serialize() for usuario in usuarios]
    return jsonify({'success': True, 'data': usuarios_serialize})

@app.route('/usuarios/<dni>', methods=["GET"])
def get_usuarios_bydni(dni):
    usuario = Usuario.query.get_or_404(dni)
    return jsonify({'success': True, 'data': usuario.serialize()})

@app.route('/usuario/login', methods=['PUT'])
def login_user():
    data = request.get_json()
    usuario = Usuario.query.get_or_404(data['dni'])
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    if data['contrasenia'] == usuario.contrasenia:
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'}), 200
    return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401

@app.route('/usuarios', methods=["POST"])
def create_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(
        dni=data['dni'],
        nombre=data['nombre'],
        apellido=data['apellido'],
        contrasenia=data['contrasenia'],
        direccion=data['direccion']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario añadido', 'data': nuevo_usuario.serialize()}), 201

@app.route('/usuarios/<dni>', methods=["PUT"])
def put_usuario(dni):
    data = request.get_json()
    usuario = Usuario.query.get_or_404(dni)
    usuario.dni = data['dni']
    usuario.nombre = data['nombre']
    usuario.apellido = data['apellido']
    usuario.contrasenia = data['contrasenia']
    usuario.direccion = data['direccion']
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario actualizado', 'data': usuario.serialize()}), 200

@app.route('/usuarios/<dni>', methods=["DELETE"])
def delete_usuario(dni):
    usuario = Usuario.query.get_or_404(dni)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario eliminado'}), 204

@app.route('/usuarios/<dni>/mascotas/', methods=["GET"])
def get_usuarios_mascotas(dni):
    usuario = Usuario.query.get_or_404(dni)
    mascotas = usuario.mascotas
    mascotas_nombres = [mascota.nombre for mascota in mascotas]
    return jsonify({'success': True, 'data': mascotas_nombres})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
