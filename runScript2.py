from datetime import timedelta, datetime, date
import requests
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import pandas as pd
from matplotlib import ticker
from matplotlib.ticker import AutoMinorLocator

addr = '0xc9becdbc62efb867cb52222b34c187fb170379c6'

end = datetime.strftime(date.today() + timedelta(days=1), '%Y-%m-%d')
start = datetime.strftime(date.today() - timedelta(days=7), '%Y-%m-%d')
timeFrame = 'hour'

u = 'https://api-v2.pendle.finance/core/v2/1/markets/' + addr + '/history?time_frame=' + timeFrame + '&timestamp_start=' + start + '&timestamp_end=' + end

r = requests.get(u)
res = r.json()['results'] # timestamp,  'underlyingInterestApy', 'underlyingRewardApy', 'underlyingApy',
                        # 'impliedApy','ytFloatingApy' ,'ptDiscount'

ts_lst = []
underlyingInterestAPY_lst = []
underlyingRewardAPY_lst = []
underlyingAPY_lst = []
impliedAPY_lst = []
longYieldAPY = []
ptPrice = []
ytPrice = []

for i in range(0, len(res)):
    ts_lst.append(res[i]['timestamp'])
    underlyingInterestAPY_lst.append(res[i]['underlyingInterestApy'])
    underlyingRewardAPY_lst.append(res[i]['underlyingRewardApy'])
    underlyingAPY_lst.append(res[i]['underlyingApy'])
    impliedAPY_lst.append(res[i]['impliedApy'])
    longYieldAPY.append(res[i]['ytFloatingApy'])
    ytPrice.append(res[i]['ptDiscount'])
    ptPrice.append(1.0 - res[i]['ptDiscount'])

with open('pendleData.pkl', 'rb') as fp:
    tmpDict = pickle.load(fp)

util_ts = []
crvUtil = []

for j in tmpDict.keys():
    util_ts.append(datetime.fromtimestamp(tmpDict[j][7]).isoformat())
    crvUtil.append(tmpDict[j][5])



l = len(util_ts)
num_labels = 9
div = math.floor((l - 2) / num_labels)

util_ts_labels = []
util_ts_labels.append(util_ts[0])
for k in range(1, num_labels):
    idx = k * div
    util_ts_labels.append(util_ts[idx])

util_ts_labels.append(util_ts[l - 1])


###################################################################################
###################################################################################

def avg_lst(lst):
    return sum(lst) / len(lst)

avg_crv_util = avg_lst(crvUtil)

def median_lst(lst):
    test_lst = lst.copy()
    test_lst.sort()
    mid = len(test_lst) // 2
    res = (test_lst[mid] + test_lst[~mid]) / 2

    return res

median_crv_util = median_lst(crvUtil)


###################################################################################
###################################################################################

sns.set_theme()
sns.set_style('whitegrid')

rng_fmt = []
rng = pd.date_range(start= util_ts[0], end=util_ts[len(util_ts) - 1], periods=12)
ticks = []
for val in rng:
    rng_fmt.append(val.isoformat()[0:10] + '\n' + val.isoformat()[11:16])
    ticks.append(val.isoformat())

fig = plt.figure(figsize=(16,8))

uopt = 0.50

u = np.empty(len(util_ts))
u.fill(uopt)
a = np.empty(len(util_ts))
a.fill(avg_crv_util)

util_df = pd.DataFrame(crvUtil, index=util_ts, columns=['Utilization'])
util_df['Util Optimal'] = u
util_df['Avg Util'] = a

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

ax.plot(util_ts, util_df)

l = len(util_ts)
twelve = math.floor(l / 12)

func = lambda x, pos: datetime.st

ax.xaxis.set_major_locator(ticker.MultipleLocator(twelve))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(func))


# ax.locator_params(axis='x', nbins=12)
#
# ax.set_xlim(util_ts[0], util_ts[len(util_ts) - 1])
#
# plt.xticks(rng_fmt)

# ax.xaxis.set_minor_locator(AutoMinorLocator())


# plt.xticks(ticks, rng_fmt)
# #
# # ax.set_xticks(ticks)
# # ax.set_xticklabels(rng_fmt)

s, e = ax.get_ylim()
ax.set_yticks(np.arange(round(s, 2), e, 0.0025))

plt.xlabel('Timestamp')
plt.ylabel('CRV Utilization Rate')

ax.legend(['Utilization', 'Optimal Util', 'Avg Utilization'])

plt.savefig('figs/util.png')
plt.savefig('content/images/util.png')


#############################################################################################


d = {
    'Timestamp': ts_lst,
    'Implied APY': impliedAPY_lst,
    'Underlying APY': underlyingAPY_lst,
    'LongYield APY': longYieldAPY,
    'PT Px': ptPrice,
    'YT Px': ytPrice
}

df = pd.DataFrame(d)

fig1 = plt.figure(figsize=(12,6))

ax1 = fig1.add_axes([0.1,0.1,0.8,0.8])

len_df = len(df['Timestamp'])
rng_ts = pd.date_range(start= df['Timestamp'][0], end=df['Timestamp'][len_df - 1], periods=12)
rng_ticks = []
rng_ts_fmt = []
for val in rng_ts:
    rng_ts_fmt.append(val.isoformat()[0:10] + '\n' + val.isoformat()[11:16])
    rng_ticks.append(val.isoformat())

ax1.plot(df['Timestamp'], df['YT Px'], color='deepskyblue')

s, e = ax1.get_ylim()
ax1.set_yticks(np.arange(round(s, 2) - 0.001,e + 0.001,0.0005))

# plt.xticks(rng_ts_fmt, rng_ticks)

ax.set_xticks(rng_ticks)
ax.set_xticklabels(rng_ts_fmt)


plt.xlabel('Timestamp')
plt.ylabel('YT Price')

plt.savefig('figs/yt_price.png')
plt.savefig('content/images/yt_price.png')


fig1 = plt.figure(figsize=(12,6))

ax1 = fig1.add_axes([0.1,0.1,0.8,0.8])

# ax1.plot(df['Timestamp'], df['PT Px'], color='red')
ax1.plot(df['Timestamp'], df['PT Px'], color='springgreen')

s, e = ax1.get_ylim()
ax1.set_yticks(np.arange(round(s, 2) + 0.0025,e + 0.0025,0.00125))


ax.set_xticks(rng_ticks)
ax.set_xticklabels(rng_ts_fmt)

plt.xlabel('Timestamp')
plt.ylabel('PT Price')

plt.savefig('figs/pt_price.png')
plt.savefig('content/images/pt_price.png')


fig1 = plt.figure(figsize=(12,6))

ax1 = fig1.add_axes([0.1,0.1,0.8,0.8])

# ax1.plot(df['Timestamp'], df['PT Px'], color='red')
ax1.plot(df['Timestamp'], df['LongYield APY'], color='deeppink')

s, e = ax1.get_ylim()
ax1.set_yticks(np.arange(round(s, 2),e,0.05))


ax.set_xticks(rng_ticks)
ax.set_xticklabels(rng_ts_fmt)

plt.xlabel('Timestamp')
plt.ylabel('Long Yield APY')

plt.savefig('figs/longYield.png')
plt.savefig('content/images/longYield.png')



fig1 = plt.figure(figsize=(14,7))

ax1 = fig1.add_axes([0.1,0.1,0.8,0.8])

# ax1.plot(df['Timestamp'], df['PT Px'], color='red')
ax1.plot(df['Timestamp'], df['Underlying APY'], color='orangered')
ax1.plot(df['Timestamp'], df['Implied APY'], color='cyan')

s, e = ax1.get_ylim()
ax1.set_yticks(np.arange(round(s, 2),e,0.0025))


ax.set_xticks(rng_ticks)
ax.set_xticklabels(rng_ts_fmt)

plt.xlabel('Timestamp')
plt.ylabel('APY')

plt.savefig('figs/underlying_implied.png')
plt.savefig('content/images/underlying_implied.png')