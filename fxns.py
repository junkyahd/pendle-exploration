from web3 import Web3
import time
import math

unixYear = 31556926

def eth_convert(val):
    return float(Web3.from_wei(val, 'ether'))

def update_now():
    return time.time()

def rateScalar(nowTime, scalar_root_eth):
    return scalar_root_eth / (nowTime / unixYear)

def yrsLeft(nowTime, expiry):
    return (expiry - nowTime) / unixYear

def rateAnchor(nowTime, lastImpliedRate, pt_ratio, expiry, scalarRoot):
    return lastImpliedRate**yrsLeft(nowTime, expiry) - ((math.log(pt_ratio/(1-pt_ratio))) / rateScalar(nowTime, scalarRoot))


