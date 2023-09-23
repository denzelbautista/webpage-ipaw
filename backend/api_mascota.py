
from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://postgres:pam645@127.0.0.1/cloudparcial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)


#modelos
class Usuario(db.Model):
    __tablename__ = 'usuario'
    dni = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)

class Mascota(db.Model):
    __tablename__ = 'mascota'
    id = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    nombre = db.Column(db.String(30), nullable=False)
    animal = db.Column(db.String(30), nullable=False)
    raza = db.Column(db.String(30), nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])

class Reserva(db.Model):
    __tablename__ = 'reserva'
    numero_reserva = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    id_mascota = db.Column(db.Integer, db.ForeignKey('mascota.id'))
    servicio = db.Column(db.String(30), nullable=False)
    f_inicio = db.Column(db.Date, nullable=False)
    f_fin = db.Column(db.Date, nullable=False)

    
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])
    mascota = db.relationship('Mascota', foreign_keys=[id_mascota])

class Ventas(db.Model):
    __tablename__ = 'ventas'
    numero_orden = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    producto = db.Column(db.String(30), nullable=False)
    fecha_orden = db.Column(db.Date, nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])

@app.route('/mascotas', methods=["GET", "POST"])
def get_post_mascotas():
  if request.method == "GET":
    mascotas = Mascota.query.all()
    return jsonify(mascotas)
  
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
     return jsonify(mascota)
  
  elif request.method == "UPDATE":
     mascota.dni_usuario = request.get_json()['dni_usuario']
     mascota.nombre = request.get_json()['nombre']
     mascota.animal = request.get_json()['animal']
     mascota.raza = request.get_json()['raza']
     db.session.commit()

  return 'SUCCESS'
   
  



if __name__ =='__main__':
    app.run(port=5000)

