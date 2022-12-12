from datetime import datetime
from flask import Flask, render_template, request, redirect
from markupsafe import escape
from search4web import search4letters, log_request
import sqlite3
import databaseFunction

app = Flask(__name__)

@app.route("/") #Ruta de la que quiero que cuelgue esta función
def hello_world() -> '302':  #Es un mensaje de redirección
   return redirect('/login') #Inicia y termina un parrafo en HTML

@app.route("/search", methods = ['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']  # Request es un diccionario y se accede a sus campos como ello
    letters = request.form['letters']
    user = request.form['user']
    result = str(search4letters(phrase,letters))
    #log_request(request,result) Para tener un archivo log, pero lo hemos cambiado por la base de datos
    databaseFunction.log_request_db(request,result,user)
    return render_template('results.html', the_title='Here are you results: ', the_phrase=phrase,
                           the_letters=letters, the_results=result)

@app.route("/entryAnonymous")
def entry_page() -> 'html': #Se le ha dicho que devulve un html
    databaseFunction.registrar_visita('Anonymous')
    most_used_phrase = databaseFunction.phrase_most_used()
    most_used_letter = databaseFunction.letters_most_used()
    return render_template('entry.html', the_title='Welcome to search for letter on web, your user is Anonymous',
                           the_user = 'Anonymous',
                           the_most_used_phrase=most_used_phrase,
                           the_most_used_letter=most_used_letter)

#Esta parte eliminarla no es normal que este en paginas web solo como depuración
@app.route("/viewlog")
def show_log() -> 'html':
    #Si se guarda el log en un archivo en la base de datos
    #with open('vsearch.log') as folder:
    #    contents = folder.read()
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute("""SELECT* FROM log""")
    contents = cursor.fetchall()
    cursor.close()
    connection.close()
    return escape(contents)


@app.route("/login")
def login() -> 'html':
    return render_template('login.html')

@app.route("/register")
def register() -> 'html':
    return render_template('register.html')

@app.route("/registerComplete", methods = ['POST'])
def registerComplete() -> 'html':
    if databaseFunction.buscarUsuario(request.form['user']):
        #El usuario existe
        return render_template('registerComplete.html', result_register='USER ALREADY EXISTS. REGISTER IS NOT COMPLETE')
    else:
        #El usuario no existe
        databaseFunction.insertarUsuario(request.form['user'],request.form['password'], request.form['email'])
        return render_template('registerComplete.html', result_register = 'COMPLETE REGISTER')

@app.route("/access", methods = ['POST'])
def access() -> 'html':
    if databaseFunction.validLogin(request.form['user'],request.form['password']):
        databaseFunction.registrar_visita(request.form['user'])
        most_used_phrase = databaseFunction.phrase_most_used()
        most_used_letter = databaseFunction.letters_most_used()
        return render_template('entry.html',
                               the_title='Welcome ' + request.form['user'] + " to search for letter on web",
                               the_user=request.form['user'],
                               the_most_used_phrase = most_used_phrase,
                               the_most_used_letter = most_used_letter)

    else:
        return render_template('error.html', the_title = "ERROR WITH THE NAME OF USER OR PASSWORD")

@app.route('/visits')
def visitas():
    connection = sqlite3.connect('BaseDataProyectos.sqlite')
    cursor = connection.cursor()
    cursor.execute("""SELECT* FROM visitas""")
    contents = cursor.fetchall()
    cursor.close()
    connection.close()
    return escape(contents)