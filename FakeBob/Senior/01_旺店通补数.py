import requests
from datetime import datetime, timedelta
import time
if __name__ == '__main__':
    start = datetime(2021, 4, 1)
    end = datetime(2021, 9, 25)
    current = start
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        # url = 'http://47.111.12.38:8080/vipStatSales/'
        # Get = {'date': '2021-01-02'}
        # x = requests.post(url, json = Get)
        x = requests.post('http://47.111.12.38:8080/vipStatSales/', json={'date': date_str})
        print('Submit Date: {} Rsp: {}'.format(date_str, x.text))
        time.sleep(10)
        current = current + timedelta(days=1)