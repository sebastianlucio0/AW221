from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "Hola, Flask"

if __name__ == "_main_":
    app.run(port=5000)
    