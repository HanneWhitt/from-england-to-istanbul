import pygsheets


#authorization
gc = pygsheets.authorize(service_file='from-england-to-istanbul-8c75e8508b5c.json')

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Sponsorship')

# #select the first sheet 
wks = sh[0]

def read():

    #Get the data from the Sheet into python as DF
    df = wks.get_as_df()

    return df

def add_new_row(df, row):
    df.loc[len(df)] = row
    return df

def write(df):
    wks.clear()
    wks.set_dataframe(df,(1,1))


df = read()

print(df)

new_row = ['Bob', 'GBP', 43.2, "WELL DONE", "bob@bob.com"]

df = add_new_row(df, new_row)

print(df)

write(df)

# # Create empty dataframe
# df = pd.DataFrame()

# # Create a column
# df['name'] = ['John', 'Steve', 'Sarah']





# #update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(df,(1,1))