# Importamos los paquetes de flask
from flask import Flask, render_template, request 
# Importar las funciones para generar hashes de contrasñea y comprobar si una contraseña coincide con un hash
from werkzeug.security import generate_password_hash

# Creamos una instancia de nuestra aplicación
app = Flask(__name__)

# Configuracion de la conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbflask'
app.secret_key = 'mysecretKey'
# Permite que FLASK vuelve a cargar las plantillas cuando se modifican 
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Craecion de ruta. La ruta / es la ruta raiz
@app.route("/")
def home():

    # Estanos retornando una vista HTML de la carpeta templates
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido_p=request.form["apellido_p"]
        apellido_m=request.form["apellido_m"]
        correo=request.form["correo"]
        password_hash = request.form["password_hash"]
        id_rol=request.form["id_rol"]

        password_hasheada = generate_password_hash(password_hash)

# Iniciamos el servidor FLASK en el puerto 5000
if __name__ == "_main_":
    app.run(port=5000)
    