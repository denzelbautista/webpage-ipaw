from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
app = Flask(__name__)

CORS(app, origins='http://127.0.0.1:5000')

# Resto de tu código aquí

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:utec@localhost:3306/ipaw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)



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
            "contrasenia":self.contrasenia,
            "direccion": self.direccion
        }


#rutas
#todos los usuarios
@app.route('/usuarios', methods=["GET"])
def get_usuarios():
  usuarios = Usuario.query.all()
  usuarios_serialize = [usuario.serialize() for usuario in usuarios]
  return jsonify({'succes':True, 'data': usuarios_serialize})

#un usuario según su dni
@app.route('/usuarios/<dni>', methods=["GET"])
def get_usuarios_bydni(dni):
  usuario = Usuario.query.get_or_404(dni)
  return jsonify(usuario)

@app.route('/usuario/login', methods = ['PUT'])
def login_user():
    data = request.get_json()
    usuario = Usuario.query.get_or_404(data['dni'])
    if not usuario:
      return 'NOT FOUND'
    if data['contrasenia'] == usuario.contrasenia:
       return 'SUCCESS'
    return 'WRONG PASSWORD'

#agregar
@app.route('/usuarios', methods = ["POST"])
def create_usuario():
   nuevo_usuario = Usuario(
      dni = request.get_json()['dni'],
      nombre  =request.get_json()['nombre'],
      apellido = request.get_json()['apellido'],
      contrasenia = request.get_json()['contrasenia'],
      direccion = request.get_json()['direccion']
   )
   db.session.add(nuevo_usuario)
   db.session.commit()
   return 'Usuario añadido :)',201

#editar
@app.route('/usuarios/<dni>', methods = ["PUT"])
def put_usuario(dni):
   usuario = Usuario.query.get_or_404(dni)
   usuario.dni = request.get_json()['dni'],
   usuario.nombre  =request.get_json()['nombre'],
   usuario.apellido = request.get_json()['apellido'],
   usuario.contrasenia = request.get_json()['contrasenia'],
   usuario.direccion = request.get_json()['direccion']
   db.session.commit()
   return 'Usuario actualizado :)',201


#eliminar un usuario
@app.route('/usuarios/<dni>', methods=["DELETE"])
def delete_usuario(dni):
  usuario = Usuario.query.get_or_404(dni)
  db.session.delete(usuario)
  db.session.commit()
  return 'SUCCESS'



@app.route('/usuarios/<dni>/mascotas/', methods=["GET"])
def get_usuarios_mascotas(dni):
  usuario = Usuario.query.get_or_404(dni)
  mascotas = usuario.mascotas
  return jsonify([mascota.nombre for mascota in mascotas])# Devuelve los nombres de las mascotas en formato JSON

if __name__ =='__main__':
    app.run(port=5001)



