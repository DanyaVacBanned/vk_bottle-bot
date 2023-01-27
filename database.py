
import sqlite3
class Database(object):

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
       
    def add_user(self, user_id, ID, name):
        with self.connection:
            self.cursor.execute('INSERT INTO users (user_id, id, name) VALUES (?, ?, ?);', (user_id,ID,name,))
            self.connection.commit()
            
    def delete_data(self, ID):
        with self.connection:
            self.cursor.execute('DELETE FROM users WHERE id = ?;', (ID,))
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
            data = self.cursor.execute("SELECT id FROM users;").fetchall()
            for row in data:
                users.append(row[0])
            return users





    #Посты
    def get_post_name(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM posts;")
            data = self.cursor.fetchall()
            for row in data:
                return row[0]
    def get_post_id(self, name):
        with self.connection:
             self.cursor.execute("SELECT id FROM posts WHERE name = ?",(name,))
             data = self.cursor.fetchall()
             for row in data:
                return row[0]
            
    def add_post(self, name):
        with self.connection:
            self.cursor.execute("INSERT INTO posts (name) VALUES (?);",(name,))
            self.connection.commit()

    def delete_post(self):
        with self.connection:
            self.cursor.execute("DELETE FROM posts;")
            self.connection.commit()
            
    #Юзеры
    def add_none_user(self,user_id):
        with self.connection:
            self.cursor.execute('INSERT INTO none_users (user_id) VALUES (?)',(user_id,))
    def select_none_users(self):
        with self.connection:
            data = self.cursor.execute('SELECT user_id FROM none_users').fetchall()
            array = []









