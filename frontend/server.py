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


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))

