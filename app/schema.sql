DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    email TEXT NOT NULL,
    ph_number TEXT,
    email_sent BOOLEAN DEFAULT 'false',
    sms_sent BOOLEAN DEFAULT 'false',
    security_question TEXT,
    security_answer TEXT,
    google_wallet_link TEXT
);

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
