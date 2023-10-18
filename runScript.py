import pendleTracker
import fxns as f

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

