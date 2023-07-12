import sqlite3
from settings import DB_NAME


def main():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    with open('create_db.sql', 'r') as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
    con.close()


if __name__ == '__main__':
    main()
