from lifetimes.utils import summary_data_from_transaction_data, calibration_and_holdout_data
from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix, plot_period_transactions, plot_calibration_purchases_vs_holdout_purchases, plot_history_alive
from lifetimes import BetaGeoFitter
import sqlite3 as sq
import pandas as pd

db = "database/8anu.db"

conn = sq.connect(db)
cur = conn.cursor()
cur.execute('SELECT user_id, date FROM ascent WHERE date>1 LIMIT 375000')

rows = cur.fetchall()

len(rows)

df = pd.DataFrame(rows, columns=['id','date'])

df.info(verbose=True)

df.nsmallest(40, 'date')
df.describe()

df['date'] = pd.to_datetime(df['date'], unit='s')

conv = summary_data_from_transaction_data(df, 'id', 'date', freq='M')

conv

bgf = BetaGeoFitter(penalizer_coef=0)
bgf.fit(conv['frequency'], conv['recency'], conv['T'])

bgf.summary
bgf.params_

# plot = plot_frequency_recency_matrix(bgf)

# prob = plot_probability_alive_matrix(bgf)

t = 1
conv['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, conv['frequency'], conv['recency'], conv['T'])
conv.sort_values(by='predicted_purchases').tail(5)

plot_period_transactions(bgf)

summary_cal_holdout = calibration_and_holdout_data(df, 'id', 'date', calibration_period_end='2010-01-01', observation_period_end='2017-01-01' )

print(summary_cal_holdout.head())

bgf.fit(summary_cal_holdout['frequency_cal'], summary_cal_holdout['recency_cal'], summary_cal_holdout['T_cal'])
plot_calibration_purchases_vs_holdout_purchases(bgf, summary_cal_holdout)


from lifetimes.plotting import plot_history_alive

id = 35
days_since_birth = 365
sp_trans = df.loc[df['id'] == id]
# sp_trans
plot_history_alive(bgf, days_since_birth, sp_trans, 'date')



conv.iloc[id]


conv.iloc[id, 2]


x = conv.idxmax(0)['frequency']
x

conv.median()['frequency']

conv.iloc[6]['frequency']

# data[data.performance==data.median()['performance']]
x = conv[conv.frequency==conv.median()['frequency']].iloc[0].name



conv

conv.loc[conv['frequency'] > 130]
