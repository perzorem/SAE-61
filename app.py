from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy storage for users (use a database in production)
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # User validation
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html', error=None)

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/newuser/', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']

        # Critères regex pour l'identifiant
        if re.match(r"^[a-z]{6,10}$", username):
            message_username = "L'identifiant respecte les critères spécifiés."
        else:
            message_username = "L'identifiant ne respecte pas les critères spécifiés."

        # Critères regex pour le mot de passe
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[%#{}@]).{6,}$", password):
            message_password = "Le mot de passe respecte les critères spécifiés."
        else:
            message_password = "Le mot de passe ne respecte pas les critères spécifiés."

        # Critères regex pour l'adresse email
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', mail):
            message_mail = "L'adresse email est valide."
        else:
            message_mail = "L'adresse email n'est pas valide."

        # Check if username is valid and unique, and password and email are valid
        if "ne respecte pas" not in message_username and "ne respecte pas" not in message_password and "n'est pas valide" not in message_mail:
            users[username] = password
            return redirect(url_for('login'))

        return render_template('newuser.html', message_username=message_username, message_password=message_password, message_mail=message_mail)

    return render_template('newuser.html', message_username=None, message_password=None, message_mail=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

