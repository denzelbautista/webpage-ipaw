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

class Mascota(db.Model):
    __tablename__ = 'mascota'
    id = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
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
        mascotas_serialize = [mascota.serialize() for mascota in mascotas]
        return jsonify({'success': True, 'data': mascotas_serialize})

    elif request.method == "POST":
        data = request.get_json()
        nueva_mascota = Mascota(dni_usuario=data['dni_usuario'], nombre=data['nombre'], animal=data['animal'], raza=data['raza'])
        db.session.add(nueva_mascota)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Mascota creada', 'data': nueva_mascota.serialize()}), 201


@app.route('/mascotas/usuario/<dni>', methods=["GET"])
def get_mascotas_por_usuario(dni):
    mascotas = Mascota.query.filter_by(dni_usuario=dni).all()
    if mascotas:
        mascotas_serialize = [mascota.serialize() for mascota in mascotas]
        return jsonify({'success': True, 'data': mascotas_serialize})
    else:
        return jsonify({'success': False, 'message': 'No se encontraron mascotas para este usuario'}), 404
        
@app.route('/mascotas/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_mascotas(id):
    mascota = Mascota.query.get_or_404(id)

    if request.method == "DELETE":
        db.session.delete(mascota)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Mascota eliminada'}), 204

    elif request.method == "GET":
        return jsonify({'success': True, 'data': mascota.serialize()})

    elif request.method == "PUT":
        data = request.get_json()
        mascota.dni_usuario = data['dni_usuario']
        mascota.nombre = data['nombre']
        mascota.animal = data['animal']
        mascota.raza = data['raza']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Mascota actualizada', 'data': mascota.serialize()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
