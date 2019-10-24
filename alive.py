from lifetimes.utils import summary_data_from_transaction_data
import sqlite3 as sq
import pandas as pd

db = "database/8anu.db"

conn = sq.connect(db)
cur = conn.cursor()
cur.execute('SELECT user_id, date FROM ascent LIMIT 1000')

rows = cur.fetchall()

df = pd.DataFrame(rows, columns=['id','date'])
df.dtypes

summary = summary_data_from_transaction_data(df, 'id', 'date', datetime_format='s')

summary
