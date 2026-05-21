import sqlite3

# Conecta ao arquivo de banco de dados (se não existir, ele cria)
conexao = sqlite3.connect("acervo.db")
cursor = conexao.cursor()

# Lê o arquivo schema.sql
with open("schema.sql", "r", encoding="utf-8") as arquivo_sql:
    sql = arquivo_sql.read()

# Executa os comandos SQL para criar a tabela
cursor.executescript(sql)

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados 'acervo.db' criado com sucesso!")