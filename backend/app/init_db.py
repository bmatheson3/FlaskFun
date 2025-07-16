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

    cursor.execute("INSERT INTO user (first_name, last_name, email) VALUES ('Blake','Matheson','blake.matheson@convergint.com')",)

    cursor.execute("INSERT INTO user (first_name, last_name, email) VALUES ('Anna','Ly','anna.ly@convergint.com')",)

    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                ('admin', hashed_password_str)
                )
    connection.commit()
    connection.close()
