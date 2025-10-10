from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Conecta ao MongoDB usando a variável de ambiente do docker-compose
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.conectaVerdeDB

@app.route('/')
def index():
    return "<h1>API ConnectGreen no ar!</h1><p>Acesse /usuarios para ver os dados.</p>"

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Acessa a collection de usuários e busca os 10 primeiros
    # O ObjectId não é serializável em JSON, então o removemos por simplicidade
    usuarios = list(db.usuarios.find({}, {'_id': 0}).limit(10))
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0')