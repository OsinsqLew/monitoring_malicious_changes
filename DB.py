import mysql.connector

class Database:
    def __init__(self, host, port, username, password):
        self.my_db = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database="ids"
            )

    def create_tables(self, file):
        self.cursor = self.my_db.cursor()
        create_commands = ''.join(file.readlines()).split('\n\n')
        for table in create_commands:
            try:
                self.cursor.execute(table)
            except mysql.connector.errors.ProgrammingError:
                continue

    def add_page():
        pass

    def update_last_hash(self, page_id):
        pass

    def last_hash(self, page_id):
        query = f"SELECT last_hash FROM ids WHERE id = {page_id};"



if __name__ == "__main__":
    db = Database("localhost", 3306, "user", "user")
    with open("create_db.txt") as create_file:
        db.create_tables(create_file)