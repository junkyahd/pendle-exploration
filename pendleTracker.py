import math
from web3 import Web3
import abi as abi_import
import time
from datetime import datetime
import fxns as f
import pprint


sy_addr = '0xE05082B184a34668CD8A904D85FA815802BBb04c'

sy_abi = abi_import.sy_token_abi

silo_addr = '0x32a4Bcd8DEa5E18a12a50584682f8E4B77fFF2DF'

siloYield = '0x96eFdF95Cc47fe90e8f63D2f5Ef9FB8B180dAeB9'

# crv
yieldToken = '0xD533a949740bb3306d119CC777fa900bA034cd52'

# crvUSD
crvUSD = '0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E'

unixYear = 31556926
t_start = datetime(2023, 10, 11, 3, 19, 11).timestamp()


mkt_abi = abi_import.mkt
mkt_addr = '0xC9beCdbC62efb867cB52222b34c187fB170379C6'

w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/HsRAh-rTKhWRIzJAVCfUU3VXFqilsfLf'))
w3.is_connected()

mkt_contract = w3.eth.contract(address=mkt_addr, abi=mkt_abi)


mkt_data_dict =  {'scalar_root': '',
    'initAnchor': '',
    'expiry': '',
    'total_pt': '',
    'total_sy': '',
    'ln_impliedRate': '',
    'lastImpliedRate': '',
    'pt_ratio': '',
    'px_ratio': '',
    'rtScalar': '',
    'rtAnchor': '',
    'exchange_rt_px': '',
    'pt_price': '',
    'sy_price': ''
}

def getMktData():
    mkt_data = mkt_contract.functions._storage().call()
    scalar_root = f.eth_convert(mkt_contract.functions.scalarRoot().call())
    initAnchor = f.eth_convert(mkt_contract.functions.initialAnchor().call())
    expiry = mkt_contract.functions.expiry().call()

    total_pt = f.eth_convert(mkt_data[0])
    total_sy = f.eth_convert(mkt_data[1])
    ln_ImpliedRate = f.eth_convert(mkt_data[2])
    lastImpliedRate = math.exp(ln_ImpliedRate)

    pt_ratio = total_pt / (total_pt + total_sy)
    px_ratio = pt_ratio / (1-pt_ratio)

    rtScalar = f.rateScalar(f.update_now(), scalar_root)
    rtAnchor = f.rateAnchor(f.update_now(), lastImpliedRate, pt_ratio, expiry, scalar_root)

    exchange_rt_px = ((math.log(pt_ratio / (1-pt_ratio))) / rtScalar) + rtAnchor


    pt_price = 1 / exchange_rt_px
    sy_price = pt_price * ((lastImpliedRate)**(f.yrsLeft(f.update_now(), expiry)) - 1)

    mkt_data_dict['scalar_root'] = scalar_root
    mkt_data_dict['initAnchor'] = initAnchor
    mkt_data_dict['expiry'] = expiry
    mkt_data_dict['total_pt'] = total_pt
    mkt_data_dict['total_sy'] = total_sy
    mkt_data_dict['ln_impliedRate'] = ln_ImpliedRate
    mkt_data_dict['lastImpliedRate'] = lastImpliedRate
    mkt_data_dict['pt_ratio'] = pt_ratio
    mkt_data_dict['px_ratio'] = px_ratio
    mkt_data_dict['rtScalar'] = rtScalar
    mkt_data_dict['rtAnchor'] = rtAnchor
    mkt_data_dict['exchange_rt_px'] = exchange_rt_px
    mkt_data_dict['pt_price'] = pt_price
    mkt_data_dict['sy_price'] = sy_price


silo_abi = abi_import.silo
silo_contract = w3.eth.contract(address=silo_addr, abi=silo_abi)

crvData = {
    'borrowAPY_crv': '',
    'depositAPY_crv': '',
    'util_crv': '',
    'liq_crv': '',
    'borrow_crv': '',
    'deposits_crv': ''
}


crvUSDData = {
    'borrowAPY_crvUSD': '',
    'depositAPY_crvUSD': '',
    'util_crvUSD': '',
    'liq_crvUSD': '',
    'borrow_crvUSD': '',
    'deposits_crvUSD': ''
}


def getCrvData():
    borrowAPY_crv = silo_contract.functions.borrowAPY(siloYield, yieldToken).call()
    depositAPY_crv = silo_contract.functions.depositAPY(siloYield, yieldToken).call()
    util_crv = silo_contract.functions.getUtilization(siloYield, yieldToken).call()
    liq_crv = silo_contract.functions.liquidity(siloYield, yieldToken).call()
    borrow_crv = silo_contract.functions.totalBorrowAmount(siloYield, yieldToken).call()
    deposits_crv = silo_contract.functions.totalDeposits(siloYield, yieldToken).call()

    crvData['borrowAPY_crv'] = f.eth_convert(borrowAPY_crv)
    crvData['depositAPY_crv'] = f.eth_convert(depositAPY_crv)
    crvData['util_crv'] = f.eth_convert(util_crv)
    crvData['liq_crv'] = f.eth_convert(liq_crv)
    crvData['borrow_crv'] = f.eth_convert(borrow_crv)
    crvData['deposits_crv'] = f.eth_convert(deposits_crv)


def getCrvUSDData():
    borrowAPY_crvUSD = silo_contract.functions.borrowAPY(siloYield, crvUSD).call()
    depositAPY_crvUSD = silo_contract.functions.depositAPY(siloYield, crvUSD).call()
    util_crvUSD = silo_contract.functions.getUtilization(siloYield, crvUSD).call()
    liq_crvUSD = silo_contract.functions.liquidity(siloYield, crvUSD).call()
    borrow_crvUSD = silo_contract.functions.totalBorrowAmount(siloYield, crvUSD).call()
    deposits_crvUSD = silo_contract.functions.totalDeposits(siloYield, crvUSD).call()

    crvUSDData['borrowAPY_crvUSD'] = f.eth_convert(borrowAPY_crvUSD)
    crvUSDData['depositAPY_crvUSD'] = f.eth_convert(depositAPY_crvUSD)
    crvUSDData['util_crvUSD'] = f.eth_convert(util_crvUSD)
    crvUSDData['liq_crvUSD'] = f.eth_convert(liq_crvUSD)
    crvUSDData['borrow_crvUSD'] = f.eth_convert(borrow_crvUSD)
    crvUSDData['deposits_crvUSD'] = f.eth_convert(deposits_crvUSD)


interestRateModel = silo_contract.functions.getModel(siloYield, crvUSD).call()

interestRateModelCRV = silo_contract.functions.getModel(siloYield, yieldToken).call()


model_abi = abi_import.model_abi
model_contract = w3.eth.contract(address=interestRateModel, abi=model_abi)

model_contract_CRV = w3.eth.contract(address=interestRateModelCRV, abi=model_abi)

iRateModel = {
    'dp': '',
    'rcomp_max': '',
    'x_max': '',
    'uopt': '',
    'ucrit': '',
    'ulow': '',
    'ki': '',
    'kcrit': '',
    'klow': '',
    'klin': '',
    'beta': '',
    'ri': '',
    'Tcrit': '',
    'config_tuple': '',
    'cb': '',
    'clin': '',
    'clow': '',
    'ccrit': '',
    'ci': ''
}

iRateModelCRV = {'dp': '','rcomp_max': '','x_max': '','uopt': '','ucrit': '','ulow': '','ki': '','kcrit': '','klow': '','klin': '','beta': '','ri': '','Tcrit': '',
              'config_tuple': '','cb': '','clin': '','clow': '','ccrit': '','ci': ''
}


def getInterestRateModelData():
    dp = model_contract.functions.DP().call()
    rcomp_max = model_contract.functions.RCOMP_MAX().call()
    x_max = model_contract.functions.X_MAX().call()

    # upot, ucrit, ulow, ki, kcrit, klow, klin, beta, ri, Tcrit
    config = model_contract.functions.getConfig(siloYield, crvUSD).call()

    uopt = config[0]
    ucrit = config[1]
    ulow = config[2]
    ki = config[3]
    kcrit = config[4]
    klow = config[5]
    klin = config[6]
    beta = config[7]
    ri = config[8]
    Tcrit = config[9]

    config_tuple = (uopt, ucrit, ulow, ki, kcrit, klow, klin, beta, ri, Tcrit)
    cb = beta * 3600
    clin = klin * 365 * 24 * 3600 * uopt
    clow = klow * 365 * 24 * 3600 * ulow
    ccrit = kcrit * 365 * 24 * 3600 * (1.0 - f.eth_convert(ulow))
    ci = ki * 365 * (24 ** 2) * (3600 ** 2) * (1.0 - f.eth_convert(uopt))

    iRateModel['dp'] = dp
    iRateModel['rcomp_max'] = rcomp_max
    iRateModel['x_max'] = x_max
    iRateModel['uopt'] = f.eth_convert(uopt)
    iRateModel['ucrit'] = f.eth_convert(ucrit)
    iRateModel['ulow'] = f.eth_convert(ulow)
    iRateModel['ki'] = ki
    iRateModel['kcrit'] = kcrit
    iRateModel['klow'] = klow
    iRateModel['klin'] = klin
    iRateModel['beta'] = beta
    iRateModel['ri'] = ri
    iRateModel[ 'Tcrit'] = Tcrit
    iRateModel['config_tuple'] = config_tuple
    iRateModel['cb'] = f.eth_convert(cb)
    iRateModel['clin'] = f.eth_convert(clin)
    iRateModel['clow'] = f.eth_convert(clow)
    iRateModel['ccrit'] = f.eth_convert(ccrit)
    iRateModel['ci'] = ci

def getInterestRateModelDataCRV():
    dp = model_contract_CRV.functions.DP().call()
    rcomp_max = model_contract_CRV.functions.RCOMP_MAX().call()
    x_max = model_contract_CRV.functions.X_MAX().call()

    # upot, ucrit, ulow, ki, kcrit, klow, klin, beta, ri, Tcrit
    config = model_contract_CRV.functions.getConfig(siloYield, yieldToken).call()

    uopt = config[0]
    ucrit = config[1]
    ulow = config[2]
    ki = config[3]
    kcrit = config[4]
    klow = config[5]
    klin = config[6]
    beta = config[7]
    ri = config[8]
    Tcrit = config[9]

    config_tuple = (uopt, ucrit, ulow, ki, kcrit, klow, klin, beta, ri, Tcrit)
    cb = beta * 3600
    clin = klin * 365 * 24 * 3600 * uopt
    clow = klow * 365 * 24 * 3600 * ulow
    ccrit = kcrit * 365 * 24 * 3600 * (1.0 - f.eth_convert(ulow))
    ci = ki * 365 * (24 ** 2) * (3600 ** 2) * (1.0 - f.eth_convert(uopt))

    iRateModelCRV['dp'] = dp
    iRateModelCRV['rcomp_max'] = rcomp_max
    iRateModelCRV['x_max'] = x_max
    iRateModelCRV['uopt'] = f.eth_convert(uopt)
    iRateModelCRV['ucrit'] = f.eth_convert(ucrit)
    iRateModelCRV['ulow'] = f.eth_convert(ulow)
    iRateModelCRV['ki'] = ki
    iRateModelCRV['kcrit'] = kcrit
    iRateModelCRV['klow'] = klow
    iRateModelCRV['klin'] = klin
    iRateModelCRV['beta'] = beta
    iRateModelCRV['ri'] = ri
    iRateModelCRV[ 'Tcrit'] = Tcrit
    iRateModelCRV['config_tuple'] = config_tuple
    iRateModelCRV['cb'] = f.eth_convert(cb)
    iRateModelCRV['clin'] = f.eth_convert(clin)
    iRateModelCRV['clow'] = f.eth_convert(clow)
    iRateModelCRV['ccrit'] = f.eth_convert(ccrit)
    iRateModelCRV['ci'] = ci



def latestBlockTS():
    return w3.eth.get_block('latest')['timestamp']

# print(currInterestRate(latestBlockTS(), update_now(), ri, util_crvUSD, Tcrit))
def calcCurrInterestRate(t0, t1, _ri, u, Tcrit):
    T = t1 - t0
    rp = 0.0
    if u > iRateModel['ucrit']:
        rp = iRateModel['kcrit'] * (iRateModel['dp'] + Tcrit + iRateModel['beta'] * T) / iRateModel['dp'] * (u - iRateModel['ucrit']) / iRateModel['dp']
    else:
        rp = min(0, iRateModel['klow'] * (u - iRateModel['ulow']) / iRateModel['dp'])

    rlin = iRateModel['klin'] * u / iRateModel['dp']
    r_i = max(_ri, rlin)
    r_i = max(r_i + iRateModel['ki'] * (u - iRateModel['uopt']) * T / iRateModel['dp'], rlin)
    rcur = max(r_i + rp, rlin) * 365 * 24 * 3600
    return rcur

getMktData()
getCrvData()
getCrvUSDData()
getInterestRateModelData()

def getCurrInterestRate(token):
    return model_contract.functions.getCurrentInterestRate(siloYield, token,  int(mkt_data_dict['expiry'])).call()


crvUSDRate = getCurrInterestRate(crvUSD)

crvRate = getCurrInterestRate(yieldToken)

longYieldRate = f.eth_convert(crvRate) - 1.0


sy_contract = w3.eth.contract(address=sy_addr, abi=sy_abi)


sy_data = {
    'rewardIndexes': '',
    'impliedUnderlyingSpread': '',
    'underlyingRate': ''
}

def getSyData():
    rewardIndexes = sy_contract.functions.rewardIndexesStored().call()[0]
    impliedUnderlyingSpread = f.eth_convert(rewardIndexes) * 10
    underlyingRate = (mkt_data_dict['lastImpliedRate'] - 1) + impliedUnderlyingSpread

    sy_data['rewardIndexes'] = rewardIndexes
    sy_data['impliedUnderlyingSpread'] = impliedUnderlyingSpread
    sy_data['underlyingRate'] = underlyingRate









def main_run():
    getMktData()
    getCrvData()
    getCrvUSDData()
    getInterestRateModelData()
    getInterestRateModelDataCRV()
    getSyData()

    print("MKT DATA: ")
    pprint.pprint(mkt_data_dict)
    print("CRV DATA: ")
    pprint.pprint(crvData)
    print("CRV USD DATA: ")
    pprint.pprint(crvUSDData)

    print("I-RATE MODEL crvUSD: ")
    pprint.pprint(iRateModel)

    print("I-RATE MODEL CRV: ")
    pprint.pprint(iRateModelCRV)


    print("SY DATA: ")
    pprint.pprint(sy_data)


    print("CRV USD RATE: ", f.eth_convert(crvUSDRate))

    print("CRV RATE: ", f.eth_convert(crvRate))

    print("LONG YIELD RATE: ", longYieldRate)


main_run()
