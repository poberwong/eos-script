# 逻辑：
# 1. 找到获取数据的 API
# 2. 解析出 eos 相关的数据
# 3. 延时循环请求，解析处理数据。
# 4. 输入需要检测的币种、价格。
# 爬取 Html，然后实时解析。
from websocket import create_connection
import gzip
import time
import json

current_price = 0

coin_type = input('please input coin, just like eosusdt or eoseth: \n')

def parseData(data):
    if ('status' in data and data['status'] == 'ok'):
        print('subscribe success: ', data['subbed'])
    else:
        current_price = data['tick']['open'] // 1
        print('open price: %f usdt \t\t\t\t close price: %f usdt' %
              (data['tick']['open'], data['tick']['open'])
             )

        if data['tick']['open'] // 1 != current_price:
            current_price = data['tick']['open'] // 1

        if data['tick']['open'] // 1 < current_price:
            print("========warning====== eos: %d" % data['tick']['open'] // 1)
        elif data['tick']['open'] // 1 > current_price:
            print("========congratulations!!!====== eos: %d" % data['tick']['open'] // 1)

if __name__ == '__main__':
    while(1):# 建立 websocket 连接
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr = json.dumps({"sub": "market." + coin_type + ".kline.1min", "id": "id10"})

    # 请求 KLine 数据
    # tradeStr="""{"req": "market.ethusdt.kline.1min","id": "id10", "from": 1513391453, "to": 1513392453}"""

    #订阅 Market Depth 数据
    # tradeStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""

    #请求 Market Depth 数据
    # tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

    #订阅 Trade Detail 数据
    # tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Trade Detail 数据
    # tradeStr="""{"req": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Market Detail 数据
    # tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""

    ws.send(tradeStr)
    while(1):
        compressData=ws.recv()
        result=gzip.decompress(compressData).decode('utf-8')
        parsed_data = json.loads(result)

        if 'ping' in parsed_data:
            pong=json.dumps({'pong': parsed_data['ping']})
            ws.send(pong)
            # ws.send(tradeStr)
        else:
            parseData(parsed_data)
