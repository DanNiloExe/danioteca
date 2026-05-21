import sqlite3

# Conecta ao banco de dados
conexao = sqlite3.connect("acervo.db")
cursor = conexao.cursor()

# Dados de teste atualizados com a nacionalidade (3º valor de cada tupla)
livros_teste = [
    ("Devoradores de Estrelas", "Andy Weir", "Americana", "Suma", "Ficção Científica", 2021, 424, "Lido"),
    ("O Hobbit", "J.R.R. Tolkien", "Britânica", "Martins Fontes", "Fantasia", 2009, 300, "Não Lido")
]

# Comando SQL de inserção atualizado com o campo nacionalidade
sql_insercao = """
INSERT INTO livros (
    titulo, autor, nacionalidade, editora, genero, ano_publicacao, num_paginas, status_leitura
) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

try:
    cursor.executemany(sql_insercao, livros_teste)
    conexao.commit()
    print("Livros de teste com nacionalidade inseridos com sucesso!")
except sqlite3.OperationalError as e:
    print(f"Erro ao inserir dados: {e}")
finally:
    conexao.close()