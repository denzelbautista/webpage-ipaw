import uuid
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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
            "contrasenia": self.contrasenia,
            "direccion": self.direccion
        }

class MascotasPerdidas(db.Model):
    __tablename__ = 'mascotas_perdidas'
    id = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: str(
        uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    nombre = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    animal = db.Column(db.String(30), nullable=False)
    raza = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(15), nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])

    def __repr__(self):
        return '<Mascotas_perdidas %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "dni_usuario": self.dni_usuario,
            "nombre": self.nombre,
            "image": self.image,
            "animal": self.animal,
            "raza": self.raza,
            "descripcion": self.descripcion,
            "estado": self.estado
        }

@app.route('/mascotas_perdidas', methods=["POST"])
def create_mascota_perdida():
    dni_usuario = request.form.get('dni_usuario')
    nombre = request.form.get('nombre')
    animal = request.form.get('animal')
    raza = request.form.get('raza')
    descripcion = request.form.get('descripcion')
    estado = request.form.get('estado')
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded!'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No image selected!'}), 400

    # Subimos la imagen al servicio de imgBB y obtenemos el nombre del archivo
    response = requests.post('https://api.imgbb.com/1/upload',
                             data={'key': '2adc25aee373fb46c2d721f17defe3d4'}, files={'image': file})

    # Obtenemos el URL de la imagen desde imgBB
    image_url = response.json()['data']['display_url']

    # Guardamos el URL de la imagen en el atributo imagen de la base de datos
    mascota_perdida = MascotasPerdidas(dni_usuario=dni_usuario, nombre=nombre, animal=animal, raza=raza,
                                       descripcion=descripcion, estado=estado, image=image_url)
    db.session.add(mascota_perdida)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Mascota perdida agregada', 'data': mascota_perdida.serialize()}), 201

@app.route('/mascotas_perdidas', methods=["GET"])
def get_mascotas_perdidas():
    mascotas = MascotasPerdidas.query.all()
    mascotas_serialize = [mascota.serialize() for mascota in mascotas]
    return jsonify({'success': True, 'data': mascotas_serialize})

@app.route('/mascotas_perdidas/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_mascota_perdida(id):
    mascota = MascotasPerdidas.query.get_or_404(id)

    if request.method == "DELETE":
        db.session.delete(mascota)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Mascota perdida eliminada'}), 204

    elif request.method == "GET":
        return jsonify({'success': True, 'data': mascota.serialize()})

    elif request.method == "PUT":
        mascota.estado = "encontrado"
        db.session.commit()
        return jsonify({'success': True, 'message': 'Mascota perdida encontrada'}), 201

    return 'SUCCESS'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003)
