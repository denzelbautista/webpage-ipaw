from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
import uuid

CORS(app, origins='http://127.0.0.1:5000')

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:1234@localhost:3306/ipaw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)


#modelos
class Usuario(db.Model):
    __tablename__ = 'usuario'
    dni = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    contrasenia = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
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

class Mascota(db.Model):
    __tablename__ = 'mascota'
    id = db.Column(db.String(36),primary_key=True,unique=True,default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    nombre = db.Column(db.String(30), nullable=False)
    animal = db.Column(db.String(30), nullable=False)
    raza = db.Column(db.String(30), nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])

    def __repr__(self):
        return '<Mascota %r>' % self.nombre
    def serialize(self):
        return {
            "id": self.id,
            "dni_usuario": self.dni_usuario,
            "nombre": self.nombre,
            "animal": self.animal,
            "raza": self.raza
        }


@app.route('/mascotas', methods=["GET", "POST"])
def get_post_mascotas():
  if request.method == "GET":
    mascotas = Mascota.query.all()
    mascotas_serialize = [mascotas.serialize() for mascotas in mascotas]
    return jsonify({'success':True, 'data':mascotas_serialize})

  elif request.method == "POST":
    nueva_mascota = Mascota(dni_usuario = request.get_json()['dni_usuario'], nombre = request.get_json()['nombre'], animal = request.get_json()['animal'], raza = request.get_json()['raza'])
    db.session.add(nueva_mascota)
    db.session.commit()
    return 'Mascota creada :)', 201

@app.route('/mascotas/<id>', methods = ['GET', 'PUT', 'DELETE'])
def get_put_delete_mascotas(id):
  mascota  = Mascota.query.get_or_404(id)
  if request.method == "DELETE":
      db.session.delete(mascota)
      db.session.commit()

  elif request.method == "GET":
     return jsonify(mascota.serialize())

  elif request.method == "UPDATE":
     mascota.dni_usuario = request.get_json()['dni_usuario']
     mascota.nombre = request.get_json()['nombre']
     mascota.animal = request.get_json()['animal']
     mascota.raza = request.get_json()['raza']
     db.session.commit()

  return 'SUCCESS'

if __name__ =='__main__':
    app.run(port=5002)
