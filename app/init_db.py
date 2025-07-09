import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')

    with open('app/schema.sql') as f:
        print(f)
        connection.executescript(f.read())
        
    cursor = connection.cursor()

    cursor.execute("INSERT INTO user (first_name, last_name, company, email, ph_number) VALUES (?, ?, ?, ?, ?)",
                ('Blake', 'Matheson', 'Convergint','blake.matheson@convergint.com','+61409961183')
                )
    cursor.execute("INSERT INTO user (first_name, last_name, company, email, ph_number) VALUES (?, ?, ?, ?, ?)",
                ('Anna', 'Ly', 'Convergint','anna.ly@convergint.com','+61424272123')
                )

    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                ('admin', 'admin')
                )


    connection.commit()
    connection.close()
