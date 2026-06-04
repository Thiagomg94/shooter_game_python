"""
Módulo que implementa o Proxy de acesso ao banco de dados de pontuações.
"""

import sqlite3

class DBProxy:
    """Proxy para operações no banco de dados SQLite de pontuações.

    Implementa o padrão Proxy: encapsula a conexão com o SQLite e expõe
    apenas as operações necessárias para o jogo (salvar e recuperar scores),
    isolando o restante do código dos detalhes de acesso a dados.

    A tabela `game_data` é criada automaticamente na primeira execução se
    ainda não existir.
    """
    def __init__(self, db_name: str):
        """Abre (ou cria) o banco de dados e garante que a tabela existe.

            Args:
                db_name: Nome do arquivo do banco de dados SQLite (sem extensão).
                Será criado no diretório de execução do jogo.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)

        # CREATE TABLE IF NOT EXISTS garante idempotência:
        # não gera erro se o banco já existia de uma sessão anterior.
        self.conn.execute('''
                            CREATE TABLE IF NOT EXISTS game_data(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            date TEXT NOT NULL)
                          ''')

    def save(self, score_dict: dict):
        """Insere um novo registro de pontuação no banco de dados.

            Usa parâmetros nomeados (:name, :score, :date) para evitar SQL Injection.

            Args:
                score_dict: Dicionário com as chaves 'name', 'score' e 'date'.
        """
        self.conn.execute('INSERT INTO game_data (name, score, date) VALUES (:name, :score, :date)', score_dict)
        self.conn.commit() # persiste a transação no arquivo

    def retrieve_top10(self) -> list:
        """Recupera os 10 melhores scores em ordem decrescente de pontuação.

            Returns:
                Lista de tuplas (id, name, score, date) com até 10 registros.
        """
        return self.conn.execute('SELECT * FROM game_data ORDER BY score DESC LIMIT 10').fetchall()

    def close(self):
        """Encerra a conexão com o banco de dados e libera recursos."""
        self.conn.close()