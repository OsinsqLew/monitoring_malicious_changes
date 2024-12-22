import mysql.connector

class Database:
    def __init__(self, host, username, password):
        self.my_db = mysql.connector.connect(host, username, password)

    def create(self, file):
        self.cursor = self.my_db.cursor()
        create_commands = file.read_lines("create_db.txt")
        self.cursor.execute(create_commands)

    def read():
        pass

    def write():
        pass

    def update_last_hash(self, page_id):
        pass

    def last_hash(self, page_id):
        pass