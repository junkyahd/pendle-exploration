import pendleTracker
import fxns as f
import time
import pickle

pendleTracker.main_run()

mkt_data = pendleTracker.mkt_data_dict
crv_data = pendleTracker.crvData

syPx = mkt_data['sy_price']
ptPx = mkt_data['pt_price']
impliedRt = mkt_data['lastImpliedRate']
crvBorrowAPY = crv_data['borrowAPY_crv']
crvDepositAPY = crv_data['depositAPY_crv']

crvUtil = crv_data['util_crv']

underlyingRt = f.eth_convert(pendleTracker.getCurrInterestRate(pendleTracker.yieldToken)) % 1

with open('pendleData.pkl', 'rb') as fp:
    pendleTracker.trackingDict = pickle.load(fp)

df_lst = [syPx, ptPx, impliedRt, crvBorrowAPY, crvDepositAPY, crvUtil, underlyingRt, time.time()]

pendleTracker.trackingDict[str(df_lst[7])] = df_lst

with open('pendleData.pkl', 'wb') as fp:
    pickle.dump(pendleTracker.trackingDict, fp)

# print(pendleTracker.trackingDict)






