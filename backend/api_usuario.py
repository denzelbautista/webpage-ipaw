
from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
import uuid
app = Flask(__name__)

# Para el login
#from flask_login import login_user,login_required,current_user,LoginManager,UserMixin, logout_user
# Para el login

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:utec@localhost:3306/cloudparcial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)

# Para el login
#login_manager = LoginManager()
#login_manager.init_app(app)
#app.secret_key = 'clave'
# Para el login

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


# USUARIO
@app.route('/usuarios', methods=["GET"])
def get_usuarios():
  usuarios = Usuario.query.all()
  usuarios_serialize = [usuarios.serialize() for usuarios in usuarios]
  return jsonify({'success':True, 'data':usuarios_serialize})  

@app.route('/usuarios', methods=["POST"])
def post_usuarios():
  nuevo_usuario = Usuario(dni = int(request.get_json()['dni']),
                          nombre = request.get_json()['nombre'], 
                          contrasenia = request.get_json()['contrasenia'],
                          apellido = request.get_json()['apellido'],
                          direccion = request.get_json()['direccion'])
  db.session.add(nuevo_usuario)
  db.session.commit()
  return 'Usuario creado :)', 201

@app.route('/usuarios/<dni>', methods=["DELETE"])
def delete_usuarios(dni):
  usuario = Usuario.query.get_or_404(dni)
  db.session.delete(usuario)
  db.session.commit()
  return 'SUCCESS'

@app.route('/usuarios/<dni>/mascotas/', methods=["GET"]) 
def get_usuarios_mascotas_perros(dni):
  usuario = Usuario.query.get_or_404(dni) 
  mascotas = usuario.mascotas 
  return jsonify([mascota.nombre for mascota in mascotas]) # Devuelve los nombres de las mascotas en formato JSON

# MASCOTAS
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


