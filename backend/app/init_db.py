import sqlite3
import bcrypt

def init_db():
    connection = sqlite3.connect('database.db')

    with open('app/schema.sql') as f:
        print(f)
        connection.executescript(f.read())
    
    password = "admin".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
        
    cursor = connection.cursor()

    # cursor.execute("INSERT INTO user (first_name, last_name, email, admin_id) VALUES ('Blake','Matheson','blake.matheson3@gmail.com', 1)",)

    # cursor.execute("INSERT INTO user (first_name, last_name, email, admin_id) VALUES ('Anna','Ly','annavyly@gmail.com', 1)",)

   
    
    cursor.execute("INSERT INTO email_template (id, subject, banner_url, content) VALUES (1, 'Welcome Email', 'https://www.convergint.com/wp-content/uploads/2021/06/logo-on-dark-blue.png', 'Hello. Welcome to our event')",)

    cursor.execute("INSERT INTO admin (username, password, email_template_id) VALUES (?, ?, 1)",
                ('admin', hashed_password_str)
                )
    
    connection.commit()
    connection.close()
