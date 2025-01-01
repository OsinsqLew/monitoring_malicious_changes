import DB
import time
import difflib
import datetime
import requests


def get_changes(db, current_version, page_id: int, date_time: str):
    last_version = db.last_version()
    changes = difflib.unified_diff(
        last_version.splitlines(), current_version.splitlines(), n=0
    )
    changes_readable = [line for line in changes if not line.startswith(("---", "+++"))]
    changes_readable = "\n".join(changes_readable)
    with open(f"changes_{page_id}_{date_time}.txt", "w", encoding="utf-8") as changes_file:
        changes_file.write(changes_readable)
    return changes_readable, changes_file


if __name__ == "__main__":
    db = DB.DataBase()
    websites = db._get_urls()
    path_base = r'C:\Users\natalcia\Desktop\PWr\ZIT\intrusion_detection_system\backup'
    while True:
        for website in websites:
            hash = DB.get_page_hash(website["url"])
            if hash == db.last_hash():
                time.sleep(60/len(websites))
                continue
            else:
                date_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                page = requests.get("https://" + website['url'])
                page = page.content
                changes = get_changes(db, page.content, website['id'], datetime)
                changes_path = path_base + f"\changes_{website['id']}_{date_time}.txt"
                page_path = path_base + f"\page{website['id']}_{date_time}.txt"
                with open(page_path, "w") as fout:
                    fout.write(page)
                db.update_last_hash(hash)
                db.add_snapshot(page_id=website['id'], hash=hash, page_path=page_path, changes_path=changes_path)
