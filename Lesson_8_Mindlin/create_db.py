import sqlite3


def create_db():
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()

    with open('ddl.sql', 'r') as file:
        statement = file.read()

    cursor.executescript(statement)

    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_db()





