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
import pandas as pd
import resend


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://127.0.0.1:5173'], 
     allow_headers=['Content-Type', 'Authorization'],
     expose_headers=['Set-Cookie'],
)
app.secret_key = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=20)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True


resend.api_key = os.environ["RESEND_API_KEY"]
print(f"Secret key: {app.secret_key}")  # Add this line to see if it's None



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

@app.route('/upload', methods=['GET','POST'])
def upload_files():
    print(request.files)
    if 'fileToUpload' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['fileToUpload']
    print(file)

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file: 
        try:
            dataFrame = pd.read_excel(file)
            data = dataFrame.to_dict(orient='records')
            print(data)
            connection = get_db_connection()
            for item in data:
                first_name = item['First Name']
                last_name = item['Last Name']
                email = item['Email']
                print(first_name,last_name,email)
                admin_id = connection.execute("SELECT id FROM admin WHERE username = ?", [session['name']]).fetchone()
                print(admin_id)
                print(admin_id[0])
                connection.execute("INSERT INTO user (first_name, last_name, email, admin_id) VALUES (?,?,?,?)",[first_name,last_name,email,admin_id[0]])
                print(f'{first_name} added to db')
                print(email)
                
                params: resend.Emails.SendParams = {
                    "from": "Acme <onboarding@resend.dev>",
                    "to": email,
                    "subject": "RSVP Form",
                    "html": "<p>http://localhost:5173/user_form</p>",
                }
                
                connection.execute("UPDATE user SET rsvp_email_sent=true WHERE email=?", [email])

                print(f"Sending email to: {email}")
                r = resend.Emails.send(params)
                print(f"Email sent successfully: {r}")

            connection.commit()
            connection.close()
            return jsonify({'message': 'File uploaded successfully', 'data': data}), 200
        except Exception as e:
            return jsonify({'Error occured:{str(e)}'}), 500
    else:
        return jsonify({'Error': 'File type not allowed'}), 400


@app.route('/login', methods=['POST'])
def admin_login():
    session.permanent = True
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    username = data.get('username')
    password = data.get('password')
    connection = get_db_connection()

    user_row = connection.execute("SELECT username, password FROM admin WHERE username = ?", [username]).fetchone()
    connection.close()
    if not user_row:
        print("user not found")
        print("incorrect pw entered")
        session['logged_in'] = False
        session.modified = True
        return jsonify({'success': False})
    
    if (bcrypt.checkpw(password.encode('utf-8'), str(user_row[1]).encode('utf-8'))):
        session['logged_in'] = True
        session['name'] = username
        session.modified = True
        
        print("=== LOGIN SUCCESS ===")
        print(f"Set session name to: {username}")
        print(f"Full session after login: {dict(session)}")
        print("====================")
        return jsonify({'success': True})
    else:
        print("incorrect pw entered")
        session['logged_in'] = False
        session.modified = True
        return jsonify({'success': False})
        

@app.route('/user_form', methods=['POST']) 
def user_form():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
        
    print(data)
    first_name = data['firstName']
    email = data['email']
    company_name = data['company']
    ph_number = data['phNumber']
    random_question = random.choice(questions['security_questions'])

    # saving info to db
    connection = get_db_connection()
    # check if correct email used
    print(connection.execute('SELECT * FROM user WHERE email=?', [email]).fetchone())
    print(email)
    if connection.execute('SELECT * FROM user WHERE email=?', [email]).fetchone() is None:
        print("Wrong email")
        # display error 
        return jsonify({"Error: Incorrect Email"}), 400
    
    connection.execute(
        'UPDATE user SET company=?, ph_number=? WHERE email=?', 
        [company_name, ph_number, email]
    )
    
    print(ph_number)
    connection.commit()

    # Step 1: Get admin_id
    admin_result = connection.execute('SELECT admin_id FROM user WHERE ph_number = ?', [ph_number]).fetchone()
    if not admin_result:
        print("No user found with this phone number")
        return

    admin_id = admin_result[0]
    print(f"Admin ID: {admin_id}")

    # Step 2: Get email_template_id
    template_result = connection.execute('SELECT email_template_id FROM admin WHERE id = ?', [admin_id]).fetchone()
    if not template_result:
        print("No admin found or no template assigned")
        return

    email_template_id = template_result[0]
    print(f"Template ID: {email_template_id}")

    # Step 3: Get all template data at once
    template_data = connection.execute('SELECT subject, content, banner_url FROM email_template WHERE id = ?', [email_template_id]).fetchone()
    if template_data:
        subject, content, banner_url = template_data
        print(f"Subject: {subject}, Content: {content}, Banner: {banner_url}")
    else:
        print("Template not found")

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": email,
        "subject": subject,
        "html": f"<img class=\"\" src=\"{banner_url}\" alt=\"banner image url\"/><p>{content}</p>",
    }
    connection.execute('UPDATE user SET welcome_email_sent=true WHERE ph_number=?', [ph_number])

    r = resend.Emails.send(params)

    generic_pass.send_security_question(first_name, ph_number, random_question)

    # Updating user's security question
    connection.execute('UPDATE user SET security_question=? WHERE email=?', [random_question,email])
    connection.commit()
    connection.close()

    return jsonify({'success': True})


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

        return render_template('users.html')
        
    return render_template('users.html')
    

@app.route('/sms_reply', methods=['GET', 'POST'])
def sms_reply():
    # resp = MessagingResponse()
    print("SMS recieved")
    
    user_ph_number = request.form['From']
    print(user_ph_number)
    

    connection = get_db_connection()    
    user_row = connection.execute('SELECT * FROM user WHERE ph_number = ?', [user_ph_number]).fetchone()
    firstName = user_row[1]
    lastName = user_row[2]
    companyName = user_row[3]
    link_sent = user_row[7]
    existing_security_answer = user_row[10]
    print(existing_security_answer)
    
    if not existing_security_answer:
        security_answer = request.values.get('Body', None)
        connection.execute('UPDATE user SET security_answer=? WHERE ph_number = ?', [security_answer, user_ph_number])
        link = generic_pass.send_pass(firstName,lastName,companyName, user_ph_number)
        connection.execute('UPDATE user SET link_sent=true where ph_number =?',[user_ph_number])  
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
        if value == 1:
            counter += 1
            
    return str(counter)

@app.route('/get_welcome_emails_sent', methods=['GET'])
def welcome_emails_sent():
    connection = get_db_connection() 
    welcome_emails_sent = connection.execute('SELECT welcome_email_sent FROM user').fetchall()

    values = [row['welcome_email_sent'] for row in welcome_emails_sent]
    counter = 0
    for value in values:
        print(values)
        if value==1:
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
        if value == 1:
            counter += 1
    return str(counter)

@app.route('/test_session')
def test_session():
    return jsonify({
        'session_data': dict(session),
        'name': session.get('name'),
        'logged_in': session.get('logged_in')
    })

@app.route('/email_template', methods=['POST', 'GET'])
def email_template():
    if(request.method == 'POST'):
        # banner, subject, content
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        connection = get_db_connection()
        try:
            banner_url = data.get('banner_url')
            subject = data.get('subject')
            content = data.get('content')
            
            connection = get_db_connection()
            existing_template_result = connection.execute('SELECT email_template_id FROM admin WHERE username = ?', [session.get('name')]).fetchone()
            
            if existing_template_result and existing_template_result[0]:
                template_id = existing_template_result[0]
                connection.execute('UPDATE email_template SET banner_url = ?, subject = ?, content = ? WHERE id = ?', 
                                    [banner_url, subject, content, template_id])
                connection.commit()
                return jsonify({'success': 'Template updated successfully'})
            else:
                return jsonify({'error': 'No template found for user'}), 404
        finally:
            connection.close()
        

    else:  # GET request
        connection = get_db_connection()
        try:
            existing_template_id = connection.execute('SELECT email_template_id FROM admin WHERE username = ?', [session['name']]).fetchone()
            print(existing_template_id)
            print(existing_template_id[0])
            if existing_template_id and existing_template_id[0]:
                template_id = existing_template_id[0]
                template_data = connection.execute('SELECT * FROM email_template WHERE id = ?', [template_id]).fetchone()
                
                if template_data:
                    response = {
                        'id': template_data[0],
                        'subject': template_data[1], 
                        'banner_url': template_data[2],
                        'content': template_data[3]
                    }
                    return jsonify(response)
            
            return jsonify({'error': 'No template found'})
        finally:
            connection.close()
        

if __name__ == '__main__':
    app.run(debug=True)