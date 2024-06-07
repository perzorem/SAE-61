import scrypt

# Replace bcrypt usage with scrypt in your script

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password, salt = user[2].split('$')
            try:
                hashed_password = scrypt.hash(password, salt.encode('utf-8'))
                if hashed_password == stored_password.encode('utf-8'):
                    session['username'] = username
                    return redirect(url_for('home'))
            except scrypt.error:
                pass
        
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)

    return render_template('login.html', error=None)

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

        if re.match(r"^[a-z]{6,10}$", username) and re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[%#{}@]).{6,}$", password) and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', mail):
            salt = bcrypt.gensalt().decode('utf-8')
            hashed_password = scrypt.hash(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
            hashed_password = f"{hashed_password}${salt}"

            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, mail))
            db.commit()
            cursor.close()

            return redirect(url_for('login'))

        return render_template('newuser.html', message_username=message_username, message_password=message_password, message_mail=message_mail)

    return render_template('newuser.html', message_username=None, message_password=None, message_mail=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

