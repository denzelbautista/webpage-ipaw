# Importar Flask
from flask import Flask, render_template

# Crear la aplicación
app = Flask(__name__)

# Definir la ruta principal
@app.route("/")
def index():
    # Renderizar el template index.html
    return render_template("index.html")

# Definir la ruta de registro
@app.route("/registro")
def registro():
    # Renderizar el template registro.html
    return render_template("registro.html")


# Ejecutar la aplicación
if __name__ == "__main__":    
    app.run(debug=True)
