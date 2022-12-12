import sqlite3
import datetime
from collections import Counter

def insertarUsuario(name,password,email):
    insertUserSQL = "INSERT INTO usuarios (name,password,email) VALUES (?, ?, ?)"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(insertUserSQL,(name,password,email))
    connection.commit()
    cursor.close()
    connection.close()

def buscarUsuario(name) -> bool:
    obtainUserSQL = """SELECT* FROM usuarios WHERE name =?"""
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(obtainUserSQL, (name,))
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False

def validLogin(name : str, password : str) -> bool:
    obtainUserSQL = """SELECT* FROM usuarios WHERE name = ?"""
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(obtainUserSQL, (name,))
    res = cursor.fetchone()
    if res:
        #Existe el usuario y se comprueba la contraseña
        if res[2] == password:
            return True
        else:
            return False
    else:
        #No existe el usuario en la base de datos
        return False

def registrar_visita(user: str) -> None:
    insertUserSQL = "INSERT INTO visitas (username) VALUES (?)"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(insertUserSQL,(user,))
    connection.commit()
    cursor.close()
    connection.close()

def log_request_db(req: 'flask_request', res: str, user: str) -> None:
    insertUserSQL = "INSERT INTO log (username,phrase,letters,remoteAddr,userAgent,result,timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(insertUserSQL, (str(req.form["user"]), str(req.form["phrase"]),str(req.form["letters"]), str(req.remote_addr), str(req.user_agent), res, str(datetime.datetime.today())))
    connection.commit()
    cursor.close()
    connection.close()

def phrase_most_used() -> str:
    obtainLettersSQL = "SELECT phrase FROM log"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(obtainLettersSQL)
    res = cursor.fetchall()
    if res:
        lista = list()
        for row in res:
            lista.append(row[0])
        return Counter(lista).most_common()[0][0]
    else:
        return ""

def letters_most_used() -> str:
    obtainLettersSQL = "SELECT letters FROM log"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(obtainLettersSQL)
    res = cursor.fetchall()
    if res:
        lista = list()
        for row in res:
            lista.append(row[0])
        return Counter(lista).most_common()[0][0]
    else:
        return ""
