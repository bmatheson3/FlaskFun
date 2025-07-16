DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    email TEXT NOT NULL,
    ph_number TEXT,
    rsvp_email_sent BOOLEAN DEFAULT 'false',
    welcome_email_sent BOOLEAN DEFAULT 'false',
    link_sent BOOLEAN DEFAULT 'false',
    security_question TEXT,
    security_answer TEXT
);

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
