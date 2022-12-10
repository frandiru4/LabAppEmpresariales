import sqlite3
import datetime

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

def log_request_db(req: 'flask_request', res: str, user: str) -> None:
    insertUserSQL = "INSERT INTO log (username,form,remoteAddr,userAgent,result,timestamp) VALUES (?,?, ?, ?, ?, ?)"
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute(insertUserSQL,(user, str(req.form), str(req.remote_addr), str(req.user_agent), res, str(datetime.datetime.today())))
    connection.commit()
    cursor.close()
    connection.close()
