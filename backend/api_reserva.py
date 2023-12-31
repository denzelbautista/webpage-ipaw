import uuid
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


class Mascota(db.Model):
    __tablename__ = 'mascota'
    id = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: str(
        uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
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
    id = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: str(
        uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    dni_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.dni'))
    id_mascota = db.Column(db.String(36), db.ForeignKey(
        'mascota.id'), nullable=False)
    servicio = db.Column(db.String(30), nullable=False)
    f_inicio = db.Column(db.DateTime, nullable=False)
    f_fin = db.Column(db.DateTime, nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[dni_usuario])
    mascota = db.relationship('Mascota', foreign_keys=[id_mascota])

    def __repr__(self):
        return '<Reserva %r>' % self.nombre

    def serialize(self):
        return {
            "dni_usuario": self.dni_usuario,
            "id_mascota": self.id_mascota,
            "servicio": self.servicio,
            "f_inicio": self.f_inicio,
            "f_fin": self.f_fin
        }


@app.route('/reservas', methods=["GET", "POST"])
def get_post_reservas():
    if request.method == 'GET':
        data = Reserva.query.all()
        serialized = [reserva.serialize() for reserva in data]
        return jsonify({'success': True, 'data': serialized})

    data = request.get_json()
    nueva = Reserva(
        dni_usuario=data['dni_usuario'],
        id_mascota=data['id_mascota'],
        servicio=data['servicio'],
        f_inicio=data['f_inicio'],
        f_fin=data['f_fin']
    )
    db.session.add(nueva)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Reserva creada con éxito', 'data': nueva.serialize()}), 201


@app.route('/reservas/<id>', methods=["GET", "PUT", "DELETE"])
def get_put_delete_reservas(id):
    data = Reserva.query.get_or_404(id)
    json = request.get_json()

    if request.method == 'GET':
        return jsonify({'success': True, 'data': data.serialize()})

    if request.method == "DELETE":
        db.session.delete(data)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Reserva eliminada'}), 204

    if request.method == "PUT":
        data.dni_usuario = json['dni_usuario']
        data.id_mascota = json['id_mascota']
        data.servicio = json['servicio']
        data.f_inicio = json['f_inicio']
        data.f_fin = json['f_fin']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Reserva actualizada', 'data': data.serialize()}), 200

    return 'SUCCESS'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
