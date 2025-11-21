# ---------------------------------------------------------------
# app.py — Servidor Flask para CyADBot
# ---------------------------------------------------------------

from flask import Flask, render_template, request, jsonify
from procesador_preguntas import ProcesadorPreguntas

app = Flask(__name__)
procesador = ProcesadorPreguntas()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"response": "No enviaste mensaje."})

    pregunta = data["message"].strip()

    if not pregunta:
        return jsonify({"response": "Escribe una pregunta."})

    respuesta = procesador.procesar_pregunta(pregunta)
    return jsonify({"response": respuesta})

if __name__ == "__main__":
    print("🚀 CyADBot corriendo en http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
