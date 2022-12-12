import sqlite3

connection = sqlite3.connect('BaseDataProyectos.sqlite')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    phrase TEXT NOT NULL,
    letters TEXT NOT NULL,
    remoteAddr TEXT NOT NULL,
    userAgent TEXT NOT NULL,
    result TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES usuarios)""")

cursor.execute("""CREATE TABLE visitas(visit INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    username TEXT NOT NULL)""")

connection.commit()
cursor.close()
connection.close()
