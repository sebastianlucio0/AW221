# Importamos los paquetes de flask
from flask import Flask, render_template, request, redirect, url_for, session, 
# Importar las funciones para generar hashes de contrasñea y comprobar si una contraseña coincide con un hash
from werkzeug.security import generate_password_hash, check_password_hash

# Creamos una instancia de nuestra aplicación
app = Flask(__name__)

#Creamos una instancia de nuestra aplicacion 
from flask_mysqldb import MySQL

# Configuracion de la conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbflask'
app.secret_key = 'mysecretKey'
# Permite que FLASK vuelve a cargar las plantillas cuando se modifican 
app.config['TEMPLATES_AUTO_RELOAD'] = True
mysql = MySQL(app)

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
        password_hash = request.form["password"]
        id_rol=request.form["id_rol"]

        password = generate_password_hash (password_hash)
        cursor = mysql.connection.cursor(
            "Select id FROM usuarios WHERE correo = %s",
            (correo,)
        )
        if cursor.fetchone():
            cursor.close()

            return render_template(
                "registro.html"                
            )            


        cursor.execute(
            """"INSERT INTO usuarios 
            (nombre,apellido_p,apellido_m,correo,password, id_rol)
            VALUES(%s,%s,%s,%s,%s)"""
        

            (
                nombre,
                apellido_p,
                apellido_m,
                correo,
                password_hash,
                id_rol,
            )
        )

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("home"))
    return render_template("registro")

#Ruta Login
@app.route("/login, method"["GET", "POSST"])
def login():

    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        #Creamos el cursor para ejecutar la consulta SQL
        cursor = mysql.connection.cursor()

    #Consultas para buscar el usuario por su correo
        sql = """
            SELECT 
            usuarios.id
            usuarios.nombre
            usuarios.apellido_p,
            usuarios.apellido_m,
            usuarios.correo
            usuarios.password
            roles.nombre
            FROM usuarios
            INER JOIN id_rol
            ON usuarios.id_rol = roles.id_rol
            WHERE usuarios.correo = %s
        """


        #Vamos a ejecutar la consulta pasando como parametro el correo 
        cursor.execute(sql,(correo,))
        usuario=cursor.fecthone()

        cursor.close()

        #Vamos a verificar la contraseña coincida con el hash
        if usuario and check_password_hash(usuario[5], password):
            session["id_usuario"] = usuario[0]
            session["nombre"] = usuario[1]
            session["rol"] = usuario[6]

            if session["rol"] == "Administrador":
                return redirect(url_for("admin"))
            return redirect (url_for("usuario"))


#Ruta de administrador
@app.route("/admin")
def admin():
    #Sin¿ no hay sesion activa lo manda al loign
    if "id_usuario" not in session:
        return redirect (url_for("login"))

#Si el rol es diferente de administrador retornara un mensaje de acceso denegado 
    if session.get("rol") != "Administrador":
        return "Acceso denegado"

#si no mandara a la vista del administrador 
    return render_template(
        "administrador.html",
        nombre=session["nombre"])
        

# Iniciamos el servidor FLASK en el puerto 5000
if __name__ == "_main_":
    app.run(port=5000)
    