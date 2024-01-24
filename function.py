import requests
from loguru import logger
from time import sleep
import json


conf = open('configs.json', 'r', encoding='utf-8').read()
confs = json.loads(conf)
bot_token = confs['bot_token']
chat_id = confs['chat_id']
clash_api = confs['clash_api']
sub_url = confs['sub_url']
airport_name = confs['airport_name']
hosting = confs['hosting']

fail_node = []


def send_message(text):
    message_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'MarkdownV2'
    }
    try:
        res = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=message_data, proxies={"http" : "http://127.0.0.1:7890"})
        if res.status_code == 200:
            logger.info(res.json())
    except Exception as e:
        logger.error(e)


def test_proxies():
    try:
        resp = requests.get(f"{clash_api}/providers/proxies")
        data = resp.json()['providers']['自动选择']['proxies']
        resp.close()
        for i in range(len(data)):
            node_name = data[i]['name']
            delay1 = data[i]['history'][0]['delay']
            delay2 = data[i]['history'][1]['delay']
            if delay1 == 0 and delay2 == 0:
                fail_node.append(''.join(node_name))
        return len(data)
    except Exception as e:
        logger.info(f"数据获取发生错误：{e}")
        sleep(3)
