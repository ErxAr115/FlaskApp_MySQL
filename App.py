from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_contacts'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def AddContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        print(fullname, phone, email)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added!')
        return redirect(url_for('Index'))    

@app.route('/edit/<string:id>')
def GetContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', contact = data[0])

@app.route('/delete/<string:id>')
def DeleteContact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Deleted')
    return redirect(url_for('Index'))

@app.route('/update/<string:id>', methods=['POST'])
def EditContact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname=%s, phone=%s, email=%s WHERE id=%s', (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contact Updated!')
        return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)