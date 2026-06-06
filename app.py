from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

tarefas = []
proximo_id = 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    global proximo_id
    dados = request.get_json()
    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400
    tarefa = {
        "id": proximo_id,
        "titulo": dados["titulo"],
        "concluida": False,
    }
    tarefas.append(tarefa)
    proximo_id += 1
    return jsonify(tarefa), 201


@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    dados = request.get_json()
    if "titulo" in dados:
        tarefa["titulo"] = dados["titulo"]
    if "concluida" in dados:
        tarefa["concluida"] = dados["concluida"]
    return jsonify(tarefa)


@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def deletar_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    tarefas.remove(tarefa)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
