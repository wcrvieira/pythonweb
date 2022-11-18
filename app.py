from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
  
  
app = Flask(__name__) 
  
  
app.secret_key = 'your secret key'
  
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perfil'
  
  
mysql = MySQL(app) 
  
  
@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM contas WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logado com sucesso !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Usuário ou senha incorretos !'
    return render_template('login.html', msg = msg) 
  
@app.route('/logout') 
def logout(): 
   session.pop('loggedin', None) 
   session.pop('id', None) 
   session.pop('username', None) 
   return redirect(url_for('login')) 
  
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'celular' in request.form and 'city' in request.form and 'state' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        celular = request.form['celular'] 
        city = request.form['city'] 
        state = request.form['state'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM contas WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Conta já existe !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Endereço de e-mail inválido !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Nome deve conter somente caracteres e números !'
        else: 
            cursor.execute('INSERT INTO contas VALUES (NULL, % s, % s, % s, % s, % s, % s)', (username, password, email, celular, city, state, )) 
            mysql.connection.commit() 
            msg = 'Você foi registrado com sucesso !'
    elif request.method == 'POST': 
        msg = 'Por favor, preencha todos os campos !'
    return render_template('register.html', msg = msg) 
  
  
@app.route("/index") 
def index(): 
    if 'loggedin' in session:  
        return render_template("index.html") 
    return redirect(url_for('login')) 
  
  
@app.route("/view") 
def view(): 
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM contas WHERE id = % s', (session['id'], )) 
        account = cursor.fetchone()     
        return render_template("view.html", account = account) 
    return redirect(url_for('login')) 
  
@app.route("/update", methods =['GET', 'POST']) 
def update(): 
    msg = '' 
    if 'loggedin' in session: 
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form: 
            username = request.form['username'] 
            password = request.form['password'] 
            email = request.form['email'] 
            celular = request.form['celular'] 
            city = request.form['city'] 
            state = request.form['state']             
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
            account = cursor.fetchone() 
            if account: 
                msg = 'Conta já existe !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                msg = 'Endereço de e-mail inválido !'
            elif not re.match(r'[A-Za-z0-9]+', username): 
                msg = 'Nome deve conter apenas caracteres e números !'
            else: 
                cursor.execute('UPDATE contas SET  username =% s, password =% s, email =% s, celular =% s, city =% s, state =% s, WHERE id =% s', (username, password, email, celular, city, state, (session['id'], ), )) 
                mysql.connection.commit() 
                msg = 'Você atualizou os dados com sucesso !'
        elif request.method == 'POST': 
            msg = 'Por favor, preencha todos os campos !'
        return render_template("update.html", msg = msg) 
    return redirect(url_for('login')) 
  
if __name__ == "__main__": 
    app.run(host ="localhost", port = int("5000")) 