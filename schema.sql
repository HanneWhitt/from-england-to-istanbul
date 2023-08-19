DROP TABLE IF EXISTS sponsorship_messages;

CREATE TABLE sponsorship_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    your_name TEXT,
    sponsorship_currency TEXT NOT NULL,
    sponsorship_amount MONEY NOT NULL,
    your_message TEXT
);