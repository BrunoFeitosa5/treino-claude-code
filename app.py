import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@contextmanager
def db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tarefas (
                    id        SERIAL PRIMARY KEY,
                    titulo    TEXT    NOT NULL,
                    concluida BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    with db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, titulo, concluida FROM tarefas ORDER BY id")
            return jsonify([dict(r) for r in cur.fetchall()])


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()
    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400
    with db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO tarefas (titulo) VALUES (%s) RETURNING id, titulo, concluida",
                (dados["titulo"],),
            )
            return jsonify(dict(cur.fetchone())), 201


@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    dados = request.get_json()
    with db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, titulo, concluida FROM tarefas WHERE id = %s", (tarefa_id,))
            tarefa = cur.fetchone()
            if tarefa is None:
                return jsonify({"erro": "Tarefa não encontrada"}), 404
            tarefa = dict(tarefa)
            novo_titulo = dados.get("titulo", tarefa["titulo"])
            nova_concluida = dados.get("concluida", tarefa["concluida"])
            cur.execute(
                "UPDATE tarefas SET titulo = %s, concluida = %s WHERE id = %s RETURNING id, titulo, concluida",
                (novo_titulo, nova_concluida, tarefa_id),
            )
            return jsonify(dict(cur.fetchone()))


@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def deletar_tarefa(tarefa_id):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tarefas WHERE id = %s RETURNING id", (tarefa_id,))
            if cur.fetchone() is None:
                return jsonify({"erro": "Tarefa não encontrada"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
