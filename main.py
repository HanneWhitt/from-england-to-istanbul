import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pygsheets


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_msg(msg_id):
    conn = get_db_connection()
    msg = conn.execute('SELECT * FROM sponsorship_messages WHERE id = ?',
                        (msg_id,)).fetchone()
    conn.close()
    if msg is None:
        abort(404)
    return msg

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySitesSecurityIsQuestionable'


@app.route('/')
def index():
    conn = get_db_connection()
    sponsorship_messages = conn.execute('SELECT * FROM sponsorship_messages').fetchall()
    print(sponsorship_messages)
    conn.close()
    return render_template('index.html', sponsorship_messages=sponsorship_messages)

@app.route('/route')
def route():
    return render_template('route.html')

@app.route('/causes')
def causes():
    return render_template('causes.html')

@app.route('/<int:msg_id>')
def msg(msg_id):
    msg = get_msg(msg_id)
    return render_template('msg.html', msg=msg)

@app.route('/post_a_message', methods=('GET', 'POST'))
def post_a_message():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                            (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('post_a_message.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))