#Imports
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

@app.route ('/login', methods=['GET'])
def login ():
  return render_template ('login.html')

@app.route ('/registro', methods=['GET'])
def registro ():
  return render_template ('registro.html')

@app.route('/registro_mascota', methods = ['GET'])
def registro_mascota():
   return render_template('mascota.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))

