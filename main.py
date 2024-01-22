###########################################
# -*- coding: utf-8 -*-                   #
# Author: @fffffx2                        #
# Date: 2024-01-23                        #
# Description: Node Health Monitor        #
###########################################
from clash import *
import schedule

headers = {'User-Agent': 'ClashforWindows/0.18.1'}


def job():
    try:
        resp = requests.get(url=sub_url, headers=headers).content
        if resp is not None:
            logger.info('配置文件获取成功!')
    except Exception as e:
        logger.error('配置文件获取失败！\n' + str(e))
        return e
    file_path = './sub.yaml'
    with open(file_path, 'wb') as f:
        f.write(resp)

    clash = Clash()
    clash.start_client()

    node_total = test_proxies()
    fail_node_str = '\n  '.join(fail_node)
    online_percentage = int((node_total - len(fail_node)) / node_total * 100)
    if len(fail_node) == 0:
        message = f'🔍 *检测报告*\n\n*周期*：30分钟\n*任务*：\\#{airport_name}节点监测\n*概要*：{node_total - len(fail_node)} / {node_total}\n*在线率*：{online_percentage}%\n*监测后端：*{hosting}\n*当前掉线节点*：\n     `无`'
    else:
        message = f'🔍 *检测报告*\n\n*周期*：30分钟\n*任务*：\\#{airport_name}节点监测\n*概要*：{node_total - len(fail_node)} / {node_total}\n*在线率*：{online_percentage}%\n*监测后端：*{hosting}\n*当前掉线节点*：\n    `' + fail_node_str + '`'
    send_message(message)
    clash.stop_client()


schedule.every(30).minutes.do(job)
while True:
    schedule.run_pending()
    sleep(3)
