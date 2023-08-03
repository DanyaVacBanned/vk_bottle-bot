import sqlite3

class Database(object):

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                name VARCHAR (150)
                );
                """
                )
            self.connection.commit()

    def add_user(self, user_id, name):
        with self.connection:
            self.cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?);', (user_id,name,))
            self.connection.commit()
            
    def delete_user(self, ID):
        with self.connection:
            self.cursor.execute('DELETE FROM users WHERE user_id = ?;', (ID,))
            self.connection.commit()
    
    def get_data(self):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM users;")
            return self.cursor.fetchall()

    def delete_all_data(self):
        with self.connection:
            self.cursor.execute("DELETE FROM users;")
            self.connection.commit()
    
    def get_users(self):
        users = []
        with self.connection:
            self.cursor.execute("SELECT * FROM users;")
            data = self.cursor.fetchall()
            for row in data:
                users.append((f'ID: {row[0]} Имя: {row[2]}'))

            return users
    def get_users_id(self):
        users =[]
        with self.connection:
            data = self.cursor.execute("SELECT user_id FROM users;").fetchall()
            for row in data:
                users.append(row[0])
            return users
        
    def get_user_by_id(self, user_id):
        with self.connection:
            user = self.cursor.execute(
                "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
            ).fetchone()
            for u in user:
                return u








