# 📚 Danioteca — Gerenciador de Acervo Pessoal

A **Danioteca** é uma aplicação web leve e moderna desenvolvida para organizar e monitorar o progresso de leituras de uma biblioteca pessoal. O sistema foi construído utilizando uma arquitetura limpa com separação de responsabilidades no backend e uma interface rica inspirada na identidade visual do projeto *FlashPoint*.

## 🎨 Interface e Identidade Visual

O design adota uma estética *Cyber-Minimalista Noturna* com foco em alta fidelidade e acabamento visual:
* **Fundo Imersivo:** Tons de preto profundo com gradientes radiais sutis.
* **Acentos de Cor:** O **Roxo Elétrico** guia o fluxo de interações principais, enquanto o **Verde Neon** destaca indicadores de sucesso e status concluídos.
* **Microinterações:** Cards de livros responsivos com efeitos dinâmicos de elevação (`hover`) e formulários de edição *inline* que se integram perfeitamente ao layout.

## 🚀 Funcionalidades Chave

* **Dashboard de Controle:** Indicadores em tempo real no topo exibindo o *Total no Acervo* e a proporção de *Livros Concluídos* (ex: `14 / 20`).
* **Operações CRUD Completas:** Cadastro, visualização, edição rápida dentro do próprio card e exclusão segura de registros.
* **Filtros Avançados Combinados:** Busca textual inteligente (por Título, Autor ou Gênero) integrada a filtros seletivos por status de leitura (*Lido*, *Lendo*, *Não Lido*).
* **Persistência Confiável:** Armazenamento estruturado através de banco de dados relacional.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python com o micro-framework [Flask](https://flask.palletsprojects.com/)
* **Banco de Dados:** [SQLite](https://www.sqlite.org/) (com queries SQL dinâmicas e prepared statements)
* **Frontend:** HTML5 (estruturação assimétrica e semântica) e CSS3 (variáveis nativas, animações de transição, CSS Grid e Flexbox)

## 📁 Estrutura do Projeto

```text
├── app.py              # Lógica do servidor Flask, rotas e consultas SQL
├── static/
│   └── style.css       # Estilização completa (Tema FlashPoint)
├── templates/
│   └── index.html      # Visão única da aplicação (Dashboard, Filtros e Grid)
├── exportar_excel      # Migrar as informações do banco para uma planilha do excel
├── danioteca_export    # Modelo de planilha preenchida
├── .gitignore          # Arquivo de proteção para não subir dados locais (.db)
└── README.md           # Documentação do projeto
```

## 🔧 Como Executar Localmente
Certifique-se de ter o Python 3.x instalado na sua máquina.

Clone este repositório:

Bash
git clone https://github.com/SEU-USUARIO/danioteca.git
cd danioteca
Instale a dependência do Flask:

Bash
pip install flask
Execute a aplicação:

Bash
python app.py
Acesse o sistema no seu navegador através do endereço
