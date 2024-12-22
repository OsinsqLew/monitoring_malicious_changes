import mysql.connector

class Database:
    def __init__(self, host, port, username, password):
        self.my_db = mysql.connector.connect(host=host, port=port, user=username, password=password)

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

if __name__ == "__main__":
    db = Database("127.0.0.1", 3306, "root", "root")
    db.create("create_db.txt")