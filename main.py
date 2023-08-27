import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import csv
from datetime import datetime
import pytz


hostname = os.uname()[1]

if hostname == 'website-vm':
    csv_file_path = '/var/www/from-england-to-istanbul/sponsorship.csv'
    image_location = '/var/www/from-england-to-istanbul/images/fundraiser.jpg'
else:
    csv_file_path = 'sponsorship_test_file.csv'
    image_location = '/mnt/c/Users/hanne/FromEnglandToIstanbul/images/fundraiser.jpg'


fieldnames = ['id', 'date', 'time', 'your_name','sponsorship_currency','sponsorship_amount','your_message','your_email']    


def read():
    pwd = os.getcwd()
    print(pwd)
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return [d for d in csv_reader]


def write_new_row(old_rows, new_dict):
    with open(csv_file_path, mode='w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames, delimiter=',')
        csv_writer.writeheader()
        for d in old_rows:
            csv_writer.writerow(d)
        csv_writer.writerow(new_dict)


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

gbp_in_usd = 1.2757
eur_in_usd = 1.090272

@app.route('/')
def index():
    sponsorship_messages = read()
    raised = 0.0
    for msg in sponsorship_messages:
        try:
            amount = float(msg['sponsorship_amount'])
            currency = msg['sponsorship_currency']
            if currency == '$':
                raised += amount
            elif currency == '£':
                raised += gbp_in_usd*amount
            elif currency == '€':
                raised += eur_in_usd*amount
        except:
            pass
    sponsorship_messages.reverse()
    return render_template('index.html', sponsorship_messages=sponsorship_messages, raised=raised, image_location=image_location)

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
		
        new_post = request.form.to_dict()

        check_pass = True

        if len(new_post['your_name']) > 70:
            flash('Please limit name field to 70 characters.')
            check_pass = False

        if not new_post['sponsorship_amount']:
            flash('Please enter a sponsorship currency and amount.')
            check_pass = False

        else:
            try:
                sa = new_post['sponsorship_amount']
                if '.' in sa:
                    dp = len(sa[sa.rfind('.')+1:])
                    if dp != 2:
                        print('dp', dp)
                        assert False
                sa = str(float(sa))
                if float(sa) > 10000 or float(sa) < 0:
                    assert False
            except:
                flash('Sponsorship amount not a valid number.')
                check_pass = False
    
        if len(new_post['your_name']) > 2000:
            flash('Sorry, my site only fits messages up to 2000 characters - but I would love to hear more from you! Please just copy and paste your text into an email to hannes.whittingham@gmail.com.')
            check_pass = False

        if len(new_post['your_email']) > 100:
            flash('Please limit email field to 100 characters.')
            check_pass = False


        if check_pass:
            
            if not new_post['your_name']:
                new_post['your_name'] = 'Anonymous'

            dt = datetime.now(pytz.timezone('Europe/London'))
            new_post['date'] = dt.strftime('%d %b %Y')
            new_post['time'] = dt.strftime('%H:%M')

            old_rows = read()
            new_post['id'] = len(old_rows)

            already_posted = False

            for old_post in old_rows:
                if old_post['your_name'] == new_post['your_name'] and old_post['sponsorship_amount'] == new_post['sponsorship_amount'] and old_post['your_message'] == new_post['your_message']:
                    already_posted = True

            if not already_posted:
                write_new_row(old_rows, new_post)

            return redirect(url_for('index'))
        
        else:
            return render_template('post_a_message.html')

    return render_template('post_a_message.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
