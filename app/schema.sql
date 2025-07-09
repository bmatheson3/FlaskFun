DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    company TEXT NOT NULL,
    email TEXT NOT NULL,
    ph_number TEXT NOT NULL,
    email_sent BOOLEAN DEFAULT 'false',
    sms_sent BOOLEAN DEFAULT 'false',
    security_question TEXT,
    security_answer TEXT
);

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
