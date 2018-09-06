from flask import Flask, jsonify, request
from model import IPANeuralNet
from io import StringIO

import configuration as conf

import pandas as pd

neuralnet = IPANeuralNet(conf.directories)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route('/')
def home():
    return jsonify(mensaje='server funcionando')


@app.route('/clasificar', methods=['GET'])
def clasificar():
    mensaje_clasificar = request.args.get('mensaje', default='', type=str)

    if mensaje_clasificar == '':
        return jsonify(error='Se debe proveer un mensaje')

    return jsonify(
        mensaje=mensaje_clasificar,
        resultado=neuralnet.make_prediction(mensaje_clasificar)
    )


@app.route('/reclasificar', methods=['POST'])
def reclasificar():
    mensaje_clasificar = request.args.get('mensaje', default='', type=str)
    conducta = request.args.get('conducta', default=0, type=int)
    epochs = request.args.get('epochs', default=1, type=int)

    if conducta == 0:
        return jsonify(error='Se debe proveer una conducta válida')

    return jsonify(
        mensaje=mensaje_clasificar,
        conducta_correcta=conducta,
        resultado=neuralnet.retrain(mensaje_clasificar, conducta, epochs)
    )


@app.route('/clasificarlote', methods=['POST'])
def clasificar_lote():
    csv = StringIO(request.get_data().decode('utf-8'))

    df = pd.read_csv(csv)
    print(df)

    return jsonify(
        mensaje='CSV Recibido'
    )


app.run(
    host=conf.server.get('address'),
    port=conf.server.get('port')
)

# app.run(
#     host='localhost',
# )

