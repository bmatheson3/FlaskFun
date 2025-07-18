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

    cursor.execute("INSERT INTO user (first_name, last_name, email) VALUES ('Blake','Matheson','blake.matheson3@gmail.com')",)

    cursor.execute("INSERT INTO user (first_name, last_name, email) VALUES ('Anna','Ly','annavyly@gmail.com')",)

    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                ('admin', hashed_password_str)
                )
    
    cursor.execute("INSERT INTO email_template (id, subject, content) VALUES (1, 'Welcome Email', 'Hello. Welcome to our event')",)
    
    connection.commit()
    connection.close()
