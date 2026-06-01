import sqlite3

class DBProxy:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.execute('''
                            CREATE TABLE IF NOT EXISTS game_data(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            date TEXT NOT NULL)
                          ''')

    def save(self, score_dict: dict):
        self.conn.execute('INSERT INTO game_data (name, score, date) VALUES (:name, :score, :date)', score_dict)
        self.conn.commit()

    def retrieve_top10(self) -> list:
        return self.conn.execute('SELECT * FROM game_data ORDER BY score DESC LIMIT 10').fetchall()

    def close(self):
        self.conn.close()