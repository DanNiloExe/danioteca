from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/capas"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def conectar_banco():
    return sqlite3.connect("acervo.db")


@app.route("/")
def index():

    termo_busca = request.args.get("busca", "").strip()
    campo_busca = request.args.get("campo", "todos").strip()
    status_busca = request.args.get("status", "").strip()

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM livros")
    total_livros = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM livros WHERE status_leitura = 'Lido'"
    )
    total_lidos = cursor.fetchone()[0]

    sql = """
        SELECT
            id,
            titulo,
            autor,
            nacionalidade,
            editora,
            genero,
            ano_publicacao,
            num_paginas,
            status_leitura,
            capa
        FROM livros
        WHERE 1=1
    """

    parametros = []

    if termo_busca:

        if campo_busca == "todos":

            sql += """
                AND (
                    LOWER(titulo) LIKE LOWER(?)
                    OR LOWER(autor) LIKE LOWER(?)
                    OR LOWER(genero) LIKE LOWER(?)
                    OR LOWER(editora) LIKE LOWER(?)
                    OR LOWER(COALESCE(nacionalidade,'')) LIKE LOWER(?)
                )
            """

            termo = f"%{termo_busca}%"

            parametros.extend([
                termo,
                termo,
                termo,
                termo,
                termo
            ])

        else:

            if campo_busca not in [
                "titulo",
                "autor",
                "genero",
                "editora"
            ]:
                campo_busca = "titulo"

            sql += f" AND LOWER({campo_busca}) LIKE LOWER(?)"
            parametros.append(f"%{termo_busca}%")

    if status_busca:
        sql += " AND status_leitura = ?"
        parametros.append(status_busca)

    cursor.execute(sql, parametros)
    livros_dados = cursor.fetchall()

    conexao.close()

    livros = []

    for row in livros_dados:
        livros.append({
            "id": row[0],
            "titulo": row[1],
            "autor": row[2],
            "nacionalidade": row[3],
            "editora": row[4],
            "genero": row[5],
            "ano_publicacao": row[6],
            "num_paginas": row[7],
            "status_leitura": row[8],
            "capa": row[9]
        })

    return render_template(
        "index.html",
        livros=livros,
        termo_atual=termo_busca,
        campo_atual=campo_busca,
        status_atual=status_busca,
        total_livros=total_livros,
        total_lidos=total_lidos
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    nacionalidade = request.form.get("nacionalidade")
    editora = request.form.get("editora")
    genero = request.form.get("genero")
    ano_publicacao = request.form.get("ano_publicacao")
    num_paginas = request.form.get("num_paginas")
    status_leitura = request.form.get("status_leitura")

    capa = request.files.get("capa")

    nome_arquivo = None

    if capa and capa.filename:

        nome_arquivo = secure_filename(capa.filename)

        caminho = os.path.join(
            app.config["UPLOAD_FOLDER"],
            nome_arquivo
        )

        capa.save(caminho)

    if not num_paginas:
        num_paginas = None

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO livros (
            titulo,
            autor,
            nacionalidade,
            editora,
            genero,
            ano_publicacao,
            num_paginas,
            status_leitura,
            capa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        titulo,
        autor,
        nacionalidade,
        editora,
        genero,
        ano_publicacao,
        num_paginas,
        status_leitura,
        nome_arquivo
    ))

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):

    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    nacionalidade = request.form.get("nacionalidade")
    editora = request.form.get("editora")
    genero = request.form.get("genero")
    ano_publicacao = request.form.get("ano_publicacao")
    num_paginas = request.form.get("num_paginas")
    status_leitura = request.form.get("status_leitura")

    capa = request.files.get("capa")

    if not num_paginas:
        num_paginas = None

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT capa FROM livros WHERE id = ?",
        (id,)
    )

    resultado = cursor.fetchone()
    capa_atual = resultado[0] if resultado else None

    nome_arquivo = capa_atual

    if capa and capa.filename:

        nome_arquivo = secure_filename(capa.filename)

        caminho = os.path.join(
            app.config["UPLOAD_FOLDER"],
            nome_arquivo
        )

        capa.save(caminho)

    cursor.execute("""
        UPDATE livros
        SET
            titulo = ?,
            autor = ?,
            nacionalidade = ?,
            editora = ?,
            genero = ?,
            ano_publicacao = ?,
            num_paginas = ?,
            status_leitura = ?,
            capa = ?
        WHERE id = ?
    """, (
        titulo,
        autor,
        nacionalidade,
        editora,
        genero,
        ano_publicacao,
        num_paginas,
        status_leitura,
        nome_arquivo,
        id
    ))

    conexao.commit()
    conexao.close()

    return redirect(f"/#visualizar-{id}")


@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM livros WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)