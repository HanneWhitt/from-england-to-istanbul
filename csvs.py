import csv

def read():
    with open('sponsorship.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return [d for d in csv_reader]
    
old_rows = read()

for d in old_rows:
    print(d)

def write_new_row(old_rows, new_row_list):
    with open('sponsorship.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['id','your_name','sponsorship_currency','sponsorship_amount','your_message','your_email'])
        for d in old_rows:
            csv_writer.writerow(d.values())
        csv_writer.writerow(new_row_list)

write_new_row(old_rows, [4, 'Hdhsjja2','reg','565656123','Test','bob@bobs.com'])