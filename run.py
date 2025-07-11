from flask import Flask, render_template, request, flash, session
from app.google_wallet import GenericPass
import os
import sqlite3
import jsonify
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.twiml.messaging_response import MessagingResponse
from app.init_db import init_db
from datetime import timedelta
import random


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

with open('questions.json', 'r') as f:
    questions = json.load(f)


init_db()

generic_pass = GenericPass()

# Connect to Database
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/get_users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    user_rows = connection.execute('SELECT * FROM user').fetchall()
    users = [tuple(row) for row in user_rows]
    print(users)
    
    connection.commmit()
    connection.close
    return json.dumps(users)

    
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def admin_login():
    session.permanent = True
    data = request.form.to_dict()
    username = data['username']
    password = data['password']
    print(username)
    connection = get_db_connection()

    user_row = connection.execute("SELECT username, password FROM admin WHERE username = ?", [username]).fetchone()
    if not user_row:
        flash("Username does not exist, please try again")
        print("incorrect pw entered")
        return index(True)


    connection.close()
    if (user_row[1] == password):
        session['logged_in'] = True
        return index()
    else:
        flash("Password incorrect, please try again")
        print("incorrect pw entered")
        return index()
        
@app.route('/user_form')
def show_form():
    return render_template('user_form.html')

@app.route('/user_form_submitted', methods=['POST']) 
def user_form():
    data = request.form.to_dict()
    first_name = data['fname']
    last_name = data['lname']
    email = data['email']
    company_name = data['company-name']
    ph_number = data['phNumber']
    random_question = random.choice(questions['security_questions'])


    # saving info to db
    connection = get_db_connection()
    # check if correct email used
    print(connection.execute('SELECT * FROM user WHERE email=?', [email]).fetchone())
    print(email)
    if connection.execute('SELECT * FROM user WHERE email=?', [email]).fetchone() is None:
        print("Wrong email")
        flash("Please enter details with email that has provided you this link")
        return show_form()
    
    connection.execute(
        'UPDATE user SET first_name=?, last_name=?, company=?, ph_number=? WHERE email=?', 
        [first_name, last_name, company_name, ph_number, email]
    )
    
    print(ph_number)
    connection.commit()
    connection.close()
    

    generic_pass.send_security_question(first_name, ph_number, random_question)

    return "Form submitted, check your SMS for a link to your pass"


@app.route('/users', methods=['GET', 'POST'])
def show_users():   
    if request.method == 'POST':
        
        # Retrieve User data from static spreadsheet
        data = request.get_json()
        
        # Provide link to redirect users to form
        link = 'http://127.0.0.1:5000/user_form'

        # Sending email
        message = Mail(
            from_email='blake.matheson3@gmail.com',
            to_emails= data['email'],
            subject= 'Welcome to Convergint',
            html_content=f'<strong>Here is the link to your pass: {link}</strong>')
        
        # COMMENTINT OUT AS EMAILS ARE GETTING BLOCKED
        # try:
        #     sg = SendGridAPIClient(os.environ.get('SEND_GRID_API_KEY'))
        #     # sg.set_sendgrid_data_residency("eu")
        #     # uncomment the above line if you are sending mail using a regional EU subuser
        #     response = sg.send(message)
        #     print(response.status_code)
        #     print(response.body)
        #     print(response.headers)
        # except Exception as e:
        #     print(e)
        return render_template('users.html')
        
    return render_template('users.html')
    

@app.route('/sms_reply', methods=['GET', 'POST'])
def sms_reply():
    # resp = MessagingResponse()
    
    user_ph_number = request.form['From']

    connection = get_db_connection()    
    user_row = connection.execute('SELECT * FROM user WHERE ph_number = ?', [user_ph_number]).fetchone()
    link = user_row[10]
    firstName = user_row[1]
    lastName = user_row[2]
    companyName = user_row[3]
    sms_sent = user_row[7]
    existing_security_answer = user_row[9]
    
    # if not security_answer:
    security_answer = request.values.get('Body', None)
    connection.execute('UPDATE user SET security_answer=? WHERE ph_number = ?', [security_answer, user_ph_number])
    generic_pass.send_pass(link,firstName,lastName,companyName, user_ph_number)
    connection.commit()
    connection.close()
    
    return "User reply with security answer received"


if __name__ == '__main__':
    app.run(debug=True)