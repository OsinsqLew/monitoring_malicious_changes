import requests
import hashlib
import DB
import time
import difflib

def get_page_hash(page):
    page_binary = page.content
    return hashlib.md5(page_binary).hexdigest()

def get_changes(db, current_version):
    last_version = db.last_version()
    changes = difflib.unified_diff(last_version.splitlines(), current_version.splitlines(), n=0)
    changes_readable = [line for line in changes if not line.startswith(('---', '+++'))]
    changes_readable = "\n".join(changes_readable)
    with open("changes.txt", "w", encoding="utf-8") as changes_file:
        changes_file.write(changes_readable)
    return changes_readable, changes_file


if __name__ == "__main__":
    print(get_page_hash("https://wp.pl"))
    urls = []
    db = DB.DataBase()
    for url in urls:
        page = requests.get(url)
        while(True):
            # sprawdzanie czy ten dzień jest już w tablicy
            hash = get_page_hash()
            if  hash == db.last_hash():
                time.sleep(30)
            else:
                db.update_last_hash(hash)




