from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)


def gerar_hash(data):
    pw_hash = bcrypt.generate_password_hash(data)
    
