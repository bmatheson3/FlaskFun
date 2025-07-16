from flask import Flask, render_template, request, flash, session, jsonify
from app.google_wallet import GenericPass
import os
import sqlite3
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.twiml.messaging_response import MessagingResponse
from app.init_db import init_db
from datetime import timedelta
import random
from flask_cors import CORS
import bcrypt


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
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
    
    connection.commit()
    connection.close()
    return json.dumps(users)

    
@app.route('/')
def index():
    return

@app.route('/login', methods=['POST'])
def admin_login():
    session.permanent = True
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    username = data.get('username')
    password = data.get('password')
    print(username)
    connection = get_db_connection()

    user_row = connection.execute("SELECT username, password FROM admin WHERE username = ?", [username]).fetchone()
    if not user_row:
        print("user not found")
        print("incorrect pw entered")
        return jsonify({'success': False})
    
    stored_password = str(user_row[1])
    print(f"Stored password in DB: '{stored_password}'")
    print(f"Length: {len(stored_password)}")
    print(f"Starts with $2b$: {stored_password.startswith('$2b$')}")


    connection.close()
    if (bcrypt.checkpw(password.encode('utf-8'), str(user_row[1]).encode('utf-8'))):
        session['logged_in'] = True
        return jsonify({'success': True})
    else:
        print("incorrect pw entered")
        session['logged_in'] = False
        return jsonify({'success': False})
        
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
        'UPDATE user SET company=?, ph_number=? WHERE email=?', 
        [company_name, ph_number, email]
    )
    
    print(ph_number)
    connection.commit()
   
    

    generic_pass.send_security_question(first_name, ph_number, random_question)

    # Updating user's security question
    connection.execute('UPDATE user SET security_question=? WHERE email=?', [random_question,email])
    connection.commit()
    connection.close()

    return "Form submitted, check your SMS!"


@app.route('/users', methods=['GET', 'POST'])
def show_users():   
    if request.method == 'POST':
        
        # Retrieve User data from static spreadsheet
        data = request.get_json()
        
        # Provide link to redirect users to form
        form_link = 'http://127.0.0.1:5000/user_form'

        # Sending email
        message = Mail(
            from_email='blake.matheson3@gmail.com',
            to_emails= data['email'],
            subject= 'Welcome to Convergint',
            html_content=f'<strong>Here is the link to your pass: {form_link}</strong>')
        
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
    firstName = user_row[1]
    lastName = user_row[2]
    companyName = user_row[3]
    link_sent = user_row[7]
    existing_security_answer = user_row[9]
    
    if not existing_security_answer:
        security_answer = request.values.get('Body', None)
        connection.execute('UPDATE user SET security_answer=? WHERE ph_number = ?', [security_answer, user_ph_number])
        link = generic_pass.send_pass(link,firstName,lastName,companyName, user_ph_number)
        connection.execute('UPDATE user SET google_wallet_link=? where ph_number =?',[link, user_ph_number])
        connection.execute('UPDATE user SET link_sent=true WHERE ph_number=?', [user_ph_number])    
        connection.commit()
        connection.close()
    
    return "Security answer received"

@app.route('/reset_all',methods=['POST'])
def reset():
    connection = get_db_connection() 
    connection.execute('UPDATE user SET first_name=NULL last_name=NULL company=NULL ph_number=NULL security_question=NULL security_answer=NULL email_sent=false link_sent=false google_wallet_link=false WHERE email=blake.matheson@convergint.com')

    connection.commit()
    connection.close()

@app.route('/get_rsvp_emails_sent', methods=['GET'])
def rsvp_emails_sent():
    connection = get_db_connection() 
    rsvp_emails_sent = connection.execute('SELECT rsvp_email_sent FROM user').fetchall()

    values = [row['rsvp_email_sent'] for row in rsvp_emails_sent]
    counter = 0
    for value in values:
        if value == 'true':
            counter += 1
            
    return str(counter)

@app.route('/get_welcome_emails_sent', methods=['GET'])
def welcome_emails_sent():
    connection = get_db_connection() 
    welcome_emails_sent = connection.execute('SELECT welcome_email_sent FROM user').fetchall()

    values = [row['welcome_email_sent'] for row in welcome_emails_sent]
    counter = 0
    for value in values:
        if value == 'true':
            counter += 1
            
    return str(counter)

@app.route('/get_security_sms_sent', methods=['GET'])
def security_questions_sent():
    connection = get_db_connection() 
    security_questions_sent = connection.execute('SELECT security_question FROM user').fetchall()

    values = [row['security_question'] for row in security_questions_sent]
    counter = 0
    for value in values:
        if value:
            counter += 1
    return str(counter)

# Only checks via sms for now as email sending does not work
@app.route('/get_links_sent', methods=['GET'])
def links_sent():
    connection = get_db_connection() 
    links_sent = connection.execute('SELECT link_sent FROM user').fetchall()

    values = [row['link_sent'] for row in links_sent]
    counter = 0
    for value in values:
        if value == 'true' :
            counter += 1
    return str(counter)

if __name__ == '__main__':
    app.run(debug=True)