from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar_banco():
    """Abre a conexão com o banco de dados."""
    return sqlite3.connect("acervo.db")

# --- ROTA PRINCIPAL: EXIBIR, FILTRAR E GERAR ESTATÍSTICAS ---
@app.route("/")
def index():
    termo_busca = request.args.get("busca", "").strip()
    campo_busca = request.args.get("campo", "titulo").strip()
    status_busca = request.args.get("status", "").strip()
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # --- NOVO: BUSCAR ESTATÍSTICAS PARA O DASHBOARD ---
    # Conta o total geral de livros cadastrados
    cursor.execute("SELECT COUNT(*) FROM livros")
    total_livros = cursor.fetchone()[0]
    
    # Conta quantos livros têm o status 'Lido'
    cursor.execute("SELECT COUNT(*) FROM livros WHERE status_leitura = 'Lido'")
    total_lidos = cursor.fetchone()[0]
    # --------------------------------------------------
    
    # Base da query SQL para listagem dos cards
    sql = "SELECT id, titulo, autor, nacionalidade, editora, genero, ano_publicacao, num_paginas, status_leitura FROM livros WHERE 1=1"
    parametros = []
    
    if termo_busca:
        if campo_busca not in ["titulo", "autor", "genero"]:
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
            "status_leitura": row[8]
        })
        
    # Enviamos também as variáveis 'total_livros' e 'total_lidos' para o HTML
    return render_template(
        "index.html", 
        livros=livros, 
        termo_atual=termo_busca, 
        campo_atual=campo_busca, 
        status_atual=status_busca,
        total_livros=total_livros,
        total_lidos=total_lidos
    )

# --- ROTA DE CADASTRO: INSERIR NOVO LIVRO NO BANCO ---
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
    
    # Garante compatibilidade do tipo numérico com o SQLite caso venha em branco
    if not num_paginas:
        num_paginas = None

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, nacionalidade, editora, genero, ano_publicacao, num_paginas, status_leitura)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (titulo, autor, nacionalidade, editora, genero, ano_publicacao, num_paginas, status_leitura))
    
    conexao.commit()
    conexao.close()
    
    return redirect("/")

# --- ROTA DE EDIÇÃO: ATUALIZAR UM LIVRO EXISTENTE ---
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
    
    if not num_paginas:
        num_paginas = None

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE livros 
        SET titulo = ?, autor = ?, nacionalidade = ?, editora = ?, genero = ?, ano_publicacao = ?, num_paginas = ?, status_leitura = ?
        WHERE id = ?
    """, (titulo, autor, nacionalidade, editora, genero, ano_publicacao, num_paginas, status_leitura, id))
    
    conexao.commit()
    conexao.close()
    
    return redirect("/")

# --- ROTA DE EXCLUSÃO: REMOVER UM LIVRO DO BANCO ---
@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    
    conexao.commit()
    conexao.close()
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)