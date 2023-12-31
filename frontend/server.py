# Imports
from flask import (
    Flask,
    render_template
)

# Configuration
app = Flask(__name__)

# Routes


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/registro', methods=['GET'])
def registro():
    return render_template('registro.html')


@app.route('/reserva', methods=['GET'])
def reserva():
    return render_template('reserva.html')


@app.route('/registro_m_perdidas', methods=['GET'])
def regmp():
    return render_template('registro_m_perdida.html')


@app.route('/registro_m', methods=['GET'])
def regm():
    return render_template('registro_m.html')


@app.route('/perros', methods=['GET'])
def perros():
    return render_template('perros.html')


@app.route('/gatos', methods=['GET'])
def gatos():
    return render_template('gatos.html')


@app.route('/aves', methods=['GET'])
def aves():
    return render_template('aves.html')


@app.route('/notfound', methods=['GET'])
def nf():
    return render_template('estamostrabajando.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
