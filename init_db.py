import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

insert_command = """INSERT INTO sponsorship_messages 
(your_name, sponsorship_currency, sponsorship_amount, your_message) 
VALUES 
(?, ?, ?, ?)
"""

initial_values = [
    ("Anonymous", "USD", 32.00, "-")
]

for msg in initial_values:
    cur.execute(insert_command, msg)

connection.commit()
connection.close()