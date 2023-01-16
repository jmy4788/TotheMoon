import sys
sys.path.insert(0, '../')

# i want to get the timestamp
import time
print(time.time())

from binance.um_futures import UMFutures
import api_key


home_key = api_key.home_key
home_secret = api_key.home_secret


client = UMFutures(key=home_key, secret=home_secret)
print(client.balance())

# 딕셔너리를 사용하는 법을 알려줘

account = client.account()
asset = account['positions']
print("************POSITION 출력************")
print(asset)

"""
"assets": [
           "assets": [
        {
            "asset": "BTC",  // asset name > 티커
            "walletBalance": "0.00241969",  // total wallet balance > 지갑 잔고
            "unrealizedProfit": "0.00000000",  // unrealized profit or loss > 미실현 손익
            "marginBalance": "0.00241969",  // margin balance > 지갑 잔고 + 미실현 손익
            "maintMargin": "0.00000000",    // maintenance margin > 포지션을 유지하기 위해 필요한 잔고
            "initialMargin": "0.00000000",  // total intial margin required with the latest mark price  > 개시 증거금
            "positionInitialMargin": "0.00000000",  // positions" margin required with the latest mark price
            "openOrderInitialMargin": "0.00000000",  // open orders" intial margin required with the latest mark price
            "maxWithdrawAmount": "0.00241969",  // available amount for transfer out
            "crossWalletBalance": "0.00241969",  // wallet balance for crossed margin
            "crossUnPnl": "0.00000000",  // total unrealized profit or loss of crossed positions
            "availableBalance": "0.00241969"  // available margin balance

            "asset": "USDT",            // asset name
            "walletBalance": "23.72469206",      // wallet balance
            "unrealizedProfit": "0.00000000",    // unrealized profit
            "marginBalance": "23.72469206",      // margin balance
            "maintMargin": "0.00000000",        // maintenance margin required
            "initialMargin": "0.00000000",    // total initial margin required with current mark price 
            "positionInitialMargin": "0.00000000",    //initial margin required for positions with current mark price
            "openOrderInitialMargin": "0.00000000",   // initial margin required for open orders with current mark price
            "crossWalletBalance": "23.72469206",      // crossed wallet balance
            "crossUnPnl": "0.00000000"       // unrealized profit of crossed positions
            "availableBalance": "23.72469206",       // available balance
            "maxWithdrawAmount": "23.72469206",     // maximum amount for transfer out
            "marginAvailable": true,    // whether the asset can be used as margin in Multi-Assets mode
            "updateTime": 1625474304765 // last update time 
        }
    # 여기 아래는 포지션
        },
        {
            "symbol": "BTCUSD_201225",
            "positionAmt":"0",
            "initialMargin": "0",
            "maintMargin": "0",
            "unrealizedProfit": "0.00000000",
            "positionInitialMargin": "0",
            "openOrderInitialMargin": "0",
            "leverage": "125",
            "isolated": false,
            "positionSide": "SHORT",  // LONG or SHORT means that it is the position of Hedge Mode 
            "entryPrice": "0.0",
            "maxQty": "50"
            "updateTime":1627026881327
        }
     ],
"""