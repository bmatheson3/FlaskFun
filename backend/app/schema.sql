DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS email_template;


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
    password TEXT NOT NULL,
    email_template_id INTEGER,
    
    FOREIGN KEY (email_template_id) REFERENCES email_template(id)
);

CREATE TABLE email_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    banner_url TEXT,
    content TEXT
);
