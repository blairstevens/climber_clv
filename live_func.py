import sqlite3 as sq
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.plotting import plot_history_alive

def imp_and_clean(db):
    conn = sq.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT user_id, date FROM ascent WHERE date>1 LIMIT 375000')
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['id','date'])
    df['date'] = pd.to_datetime(df['date'], unit='s')
    return df

def convert_to_summary(df):
    conv = summary_data_from_transaction_data(df, 'id', 'date', freq='M')
    return conv

def fit_clv(conv, coef):
    bgf = bgf = BetaGeoFitter(penalizer_coef=coef)
    bgf.fit(conv['frequency'], conv['recency'], conv['T'])
    return bgf

def plot_hist_best_freq(bgf,conv,df):
    id = conv.idxmax()['frequency']
    days_since_birth = 365
    sp_trans = df.loc[df['id'] == id]
    return plot_history_alive(bgf, days_since_birth, sp_trans, 'date')

def plot_hist_median_freq(bgf,conv,df):
    id = conv[conv.frequency==conv.median()['frequency']].iloc[0].name
    days_since_birth = 365
    sp_trans = df.loc[df['id'] == id]
    return plot_history_alive(bgf, days_since_birth, sp_trans, 'date')

db = "database/8anu.db"

df = imp_and_clean(db)

conv = convert_to_summary(df)

bgf = fit_clv(conv, 0.01)

plot_hist_best_freq(bgf,conv,df)

plot_hist_median_freq(bgf,conv,df)
