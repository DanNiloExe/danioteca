import sqlite3
import pandas as pd
from datetime import datetime

def exportar_banco_para_excel():
    try:
        # 1. Ajustado para o nome exato do seu banco da Danioteca
        nome_banco = "acervo.db" 
        conexao = sqlite3.connect(nome_banco)
        
        # 2. Query para trazer todo o seu acervo
        query = "SELECT * FROM livros"
        
        # 3. O Pandas lê o banco e mapeia as colunas automaticamente
        df = pd.read_sql_query(query, conexao)
        
        # 4. Fecha a conexão com segurança
        conexao.close()
        
        # Verifica se há dados cadastrados
        if df.empty:
            print("⚠️ O seu acervo em 'acervo.db' está vazio. Cadastre livros pelo navegador antes de exportar!")
            return
            
        # 5. Gera o nome do arquivo com a data de hoje
        data_atual = datetime.now().strftime("%Y-%m-%d")
        nome_arquivo = f"danioteca_export_{data_atual}.xlsx"
        
        # 6. Salva a planilha formatada na raiz do projeto
        df.to_excel(nome_arquivo, index=False)
        print(f"🎉 Sucesso! Seu acervo foi exportado com segurança para o arquivo: '{nome_arquivo}'")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Erro operacional do SQLite: {e}")
        print("Certifique-se de que o script está na mesma pasta que o arquivo 'acervo.db'.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    exportar_banco_para_excel()