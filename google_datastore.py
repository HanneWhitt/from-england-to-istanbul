from google.cloud import datastore

datastore_client = datastore.Client()

def store_message(row):
    entity = datastore.Entity(key=datastore_client.key("message"))
    entity.update(row)
    datastore_client.put(entity)


def fetch_messages(limit=None):
    query = datastore_client.query(kind="message")
    query.order = ["id"]
    times = query.fetch(limit=limit)
    return times

#id,your_name,sponsorship_currency,sponsorship_amount,your_message,your_email

r1 = {
    'id': 4,
    'your_name': 'Hdhsjja2',
    'sponsorship_currency': 'GBP',
    'sponsorship_amount': '565656123',
    'your_message': 'you r wally',
    'your_email': 'bob@bobs.com'
}

r2 = {
    'id': 5,
    'your_name': 'Hdhsjja2',
    'sponsorship_currency': 'GBP',
    'sponsorship_amount': '565656123',
    'your_message': 'you r wally',
    'your_email': 'bob@bobs.com'
}

store_message(r1)
store_message(r2)

for thing in fetch_messages():
    print(thing)