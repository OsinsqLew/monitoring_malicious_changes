import mysql.connector
import requests
import hashlib
import logging
from datetime import date, datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
logger.addHandler(sh)


def get_page_hash(url):
    page = requests.get("https://" + url)
    page_binary = page.content
    return hashlib.md5(page_binary).hexdigest().strip()


class Database:
    def __init__(self, host, port, username, password):
        self.my_db = mysql.connector.connect(
            host=host, port=port, user=username, password=password, database="ids"
        )

    def create_tables(self, file):
        cursor = self.my_db.cursor()
        create_commands = "".join(file.readlines()).split("\n\n")
        for table in create_commands:
            try:
                cursor.execute(table)
            except mysql.connector.errors.ProgrammingError:
                continue
        cursor.close()

    def add_snapshot(self, page_id, hash, page_path, changes_path):
        cursor = self.my_db.cursor()
        query_snapshots = f"INSERT INTO snapshots (website_id, day, hour, hash, page_body, changes) VALUES ('{page_id}', '{date.today().strftime("%d-%m-%Y")}', '{datetime.now().time()}', '{hash}', '{page_path}', '{changes_path}')"
        try:
            cursor.execute(query_snapshots)
            logger.info(f"Snapshot for page {page_id} added successfully.")
            self.my_db.commit()
        except Exception as e:
            logger.info(f"Error adding snapshot: {e}")
            self.my_db.rollback()
        finally:
            cursor.close()

    def add_page(self, url: str, page_path, changes_path):
        cursor = self.my_db.cursor()
        hash = get_page_hash(url)
        query_websites = (
            f"INSERT INTO websites (url, last_hash) VALUES ('{url}', '{hash}');"
        )
        try:
            cursor.execute(query_websites)
            page_id = cursor.lastrowid  # * gets the last inserted row's id
            query_snapshots = f"INSERT INTO snapshots (website_id, day, hour, hash, page_body, changes) VALUES ('{page_id}', '{date.today().strftime("%d-%m-%Y")}', '{datetime.now().time()}', '{hash}', '{page_path}', '{changes_path}')"
            cursor.execute(query_snapshots)
            self.my_db.commit()
            logger.info(f"Page {url} added successfully.")
        except Exception as e:
            logger.info(f"Error adding page: {e}")
            self.my_db.rollback()
        finally:
            cursor.close()

    def get_urls(self):
        cursor = self.my_db.cursor(dictionary=True)
        query = "SELECT id, url FROM websites"
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logger.info(f"Got {len(result)} urls.")
        except Exception as e:
            logger.info(f"Error getting urls: {e}")
        finally:
            cursor.close()
        return result

    def update_last_hash(self, page_id: int, hash: str):
        cursor = self.my_db.cursor()
        query = f"UPDATE websites SET last_hash = '{hash}' WHERE id = {page_id}"
        try:
            cursor.execute(query)
            logger.info(f"Updated page: {page_id} hash.")
            self.my_db.commit()
        except Exception as e:
            logger.info(f"Error getting last hash: {e}")
            self.my_db.rollback()
        finally:
            cursor.close()

    def last_hash(self, page_id: int):
        cursor = self.my_db.cursor()
        query = f"SELECT last_hash FROM websites WHERE id = {page_id};"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            logger.info(f"Error getting last hash: {e}")
            cursor.close()


if __name__ == "__main__":
    db = Database("localhost", 3306, "user", "user")
    db.add_page("dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html", "123")
    # urls = db._get_urls()
    # print(urls)
    # for url in urls:
    #     print(url["id"])

    # with open("create_db.txt") as create_file:
    #     db.create_tables(create_file)
