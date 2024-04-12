from trading_ig import IGService
from trading_ig.config import config
from trading_ig.rest import IGService, ApiExceededException
from tenacity import Retrying, wait_exponential, retry_if_exception_type
import requests_cache
from datetime import datetime, timedelta


retryer = Retrying(wait=wait_exponential(),
    retry=retry_if_exception_type(ApiExceededException))
#ig_service = IGService(config.username, config.password, config.api_key, retryer=retryer)

ig_service = IGService(config.username, config.password, config.api_key, config.acc_type)
ig_service.create_session()

session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=timedelta(hours=1))

#account_info = ig_service.switch_account(config.acc_number, False) # not necessary
#print(account_info)

open_positions = ig_service.fetch_open_positions()
#print("open_positions:\n%s" % open_positions)

print("")

#epic = 'CS.D.EURUSD.TODAY.IP'
resolution = 'D'
num_points = 10
response = ig_service.fetch_historical_prices_by_epic_and_num_points('CS.D.EURUSD.TODAY.IP', resolution, num_points)
df_ask = response['prices']['ask']
#print("ask prices:\n%s" % df_ask)

results = ig_service.search_markets("Japan 225")#获取市场

#print(type(results['epic'].loc[0]))

#print(results)

#print(results['epic'].loc[0])
market = ig_service.fetch_market_by_epic('CS.D.USCGC.TODAY.IP')

stocks=['US 500', 'Japan 225', 'USD/SGD', 'GBP/USD', 'EUR/USD', 'Germany 40', 'Taiwan Index', 'Australia 200', 'HK 50',
        'USD/JPY', 'FTSE 100', 'France 40', 'EMFX USD/INR', 'USD/CHN', 'EMFX USD/TWD', 'AUD/USD', 'EMFX USD/KRW',
        'USD/MXN']

markets=[]
for stock in stocks:
    results = ig_service.search_markets(stock)
    markets.append(results['epic'].loc[0])
#print(markets)


for market in markets:
    result = ig_service.fetch_historical_prices_by_epic(market, '1H', '2023-11-08', '2023-11-09')
    print(result)


#result = ig_service.fetch_historical_prices_by_epic('IX.D.SPTRD.IFD.IP','1H','2023-11-08', '2023-11-09')#输出对应时间的股票价格
#yyyy-MM-dd'T'HH:mm:ss


#result = ig_service.fetch_historical_prices_by_epic_and_date_range('IX.D.SPTRD.IFD.IP',resolution,'2020:09:01-00:00:00','2020:09:01-04:00:00',session)

#session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=timedelta(hours=1))
#result  = ig_service.fetch_historical_prices_by_epic_and_date_range('IX.D.SPTRD.IFD.IP', '1H', '2023-09-01 00:00:00', '2023-09-02 00:00:00', session)

#print(result['prices'])