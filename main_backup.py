import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import csv




def store_message(row):
    entity = datastore.Entity(key=datastore_client.key("message"))
    entity.update(row)
    datastore_client.put(entity)


def fetch_messages(limit=None):
    query = datastore_client.query(kind="message")
    query.order = ["id"]
    times = query.fetch(limit=limit)
    return times

def read():
    with open('sponsorship.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return [d for d in csv_reader]
    

def write_new_row(old_rows, new_row_list):
    with open('sponsorship.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['id','your_name','sponsorship_currency','sponsorship_amount','your_message','your_email'])
        for d in old_rows:
            csv_writer.writerow(d.values())
        csv_writer.writerow(new_row_list)


def get_worksheet():

    import pygsheets

    #authorization
    gc = pygsheets.authorize(service_file='from-england-to-istanbul-8c75e8508b5c.json')

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Sponsorship')

    # #select the first sheet 
    wks = sh[0]

    return wks


def read_from_gsheet():

    wks = get_worksheet()

    #Get the data from the Sheet into python as DF
    df = wks.get_as_df()

    return df

def write_to_gsheet(df):
    wks = get_worksheet()
    wks.clear()
    wks.set_dataframe(df,(1,1))


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
    sponsorship_messages = read()
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
			
        your_name = request.form['your_name']

        print(your_name)
        sponsorship_currency = request.form['sponsorship_currency']
        print(sponsorship_currency)
        sponsorship_amount = request.form['sponsorship_amount']
        print(sponsorship_amount)

        your_message = request.form['your_message']
        your_email = request.form['your_email']

        if not sponsorship_amount:
            flash('Sponsorship amount is required!')
        else:
            rows = read()
            new_id = len(rows)
            new_row = [new_id, your_name, sponsorship_currency, sponsorship_amount, your_message, your_email]
            write_new_row(rows, new_row)
        return redirect(url_for('index'))

    return render_template('post_a_message.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
