import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')

    with open('app/schema.sql') as f:
        print(f)
        connection.executescript(f.read())
        
    cursor = connection.cursor()

    cursor.execute("INSERT INTO user (email) VALUES (?)",
                ('blake.matheson@convergint.com',)
                )
    cursor.execute("INSERT INTO user (email) VALUES (?)",
                ('anna.ly@convergint.com',)
                )

    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                ('admin', 'admin')
                )


    connection.commit()
    connection.close()
