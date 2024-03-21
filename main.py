###########################################
# -*- coding: utf-8 -*-                   #
# Author: @fffffx2                        #
# Date: 2024-01-23                        #
# Description: Node Health Monitor        #
###########################################
from clash import *
import schedule


banner = """
 ________  ________  ________  ________  ________  ____  ____   _____   
|_   __  ||_   __  ||_   __  ||_   __  ||_   __  ||_  _||_  _| / ___ `. 
  | |_ \_|  | |_ \_|  | |_ \_|  | |_ \_|  | |_ \_|  \ \  / /  |_/___) | 
  |  _|     |  _|     |  _|     |  _|     |  _|      > `' <    .'____.' 
 _| |_     _| |_     _| |_     _| |_     _| |_     _/ /'`\ \_ / /_____  
|_____|   |_____|   |_____|   |_____|   |_____|   |____||____||_______| 

TG频道 @fffffx2                                                           
"""

print(banner + '\n节点检测程序开始运行')
headers = {'User-Agent': 'ClashforWindows/0.18.1'}


def download_geoip_metadb(directory):
    file_path = os.path.join(directory, 'geoip.metadb')
    url = 'https://file.xn--4gqs5ymhk43c.eu.org/geoip.metadb'

    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(file_path):
        try:
            resp = requests.get(url).content
            with open(file_path, 'wb') as f:
                f.write(resp)
            logger.info(f'成功下载 geoip.metadb 文件到 {directory}')
        except Exception as e:
            logger.error(f'下载 geoip.metadb 文件失败！\n{str(e)}')
            return e
    else:
        pass


def download_client(directory):
    file_path = os.path.join(directory, 'mihomo')
    url = 'https://file.xn--4gqs5ymhk43c.eu.org/mihomo'

    if not os.path.exists(file_path):
        try:
            resp = requests.get(url).content
            with open(file_path, 'wb') as f:
                f.write(resp)
            logger.info(f'成功下载 mihomo 客户端到 {directory}')
        except Exception as e:
            logger.error(f'下载 mihomo 客户端失败！\n{str(e)}')
            return e
    else:
        pass


def job():
    mihomo_dir = f'{os.getcwd()}'
    download_client(mihomo_dir)

    geoip_dir = '/root/.config/mihomo'
    download_geoip_metadb(geoip_dir)
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


job()
schedule.every(30).minutes.do(job)
while True:
    schedule.run_pending()
    sleep(3)
