CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    nacionalidade TEXT,
    editora TEXT,
    genero TEXT NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    num_paginas INTEGER,
    status_leitura TEXT DEFAULT 'Não Lido',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);