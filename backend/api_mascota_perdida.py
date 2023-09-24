
#api mascotas perdidas

from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:utec@localhost:3306/cloudparcial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crea una instancia de SQLAlchemy
db = SQLAlchemy(app)


#modelos
#por si acaso el del usuario aunque aqui se puede eliminar dependiendo si agregan una ruta que lo necesite :)
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

class Mascotas_perdidas(db.Model):
    __tablename__ = 'mascotas_perdidas'
    id = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    nombre = db.Column(db.String(30), nullable=False)
    animal = db.Column(db.String(30), nullable=False)
    raza = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(200), nullable = False)
    estado = db.Column(db.String(15), nullable = False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])

    def __repr__(self):
        return '<Mascotas_perdidas %r>' % self.nombre
    def serialize(self):
        return {
            "id": self.id,
            "dni_usuario": self.dni_usuario,
            "nombre": self.nombre,
            "animal": self.animal,
            "raza": self.raza,
            "descripcion":self.descripcion,
            "estado": self.estado
        }

@app.route('/mascotas_perdidas', methods=["GET", "POST"])
def get_post_mascotas_perdidas():
  if request.method == "GET":
    mascotas = Mascotas_perdidas.query.all()
    mascotas_serialize = [mascota.serialize() for mascota in mascotas]
    return jsonify({'succes':True, 'data':mascotas_serialize})
  
  elif request.method == "POST":
    nueva_mascota = Mascotas_perdidas(dni_usuario = request.get_json()['dni_usuario'], nombre = request.get_json()['nombre'], animal = request.get_json()['animal'], raza = request.get_json()['raza'],
                                      descripcion = request.get_json()['descripcion'], estado = "perdido")
    db.session.add(nueva_mascota)
    db.session.commit()
    return 'Mascota perdida agregada :C', 201
  

@app.route('/mascotas_perdidas/<id>', methods = ['GET', 'PUT', 'DELETE'])
def get_put_delete_mascotas_perdidas(id):
  mascota  = Mascotas_perdidas.query.get_or_404(id)
  if request.method == "DELETE":
      db.session.delete(mascota)
      db.session.commit()

  elif request.method == "GET":
     return jsonify(mascota.serialize())
  
  elif request.method == "UPDATE":#para el boton de encontrado
     mascota.estado = "encontrado"
     db.session.commit()
     return 'Mascota perdida ha sido encontrada :)', 201

  return 'SUCCESS'
   


if __name__ =='__main__':
    app.run(port=5000)

