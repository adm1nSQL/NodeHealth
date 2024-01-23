import os
import subprocess
import sys
import time
import signal
import psutil
from function import *


class Clash(object):
    def __init__(self):
        self._process = None
        self._pid = None

    def start_client(self):
        try:
            # 检查端口是否被占用，如果被占用则终止对应进程
            self._check_and_terminate_process(self, 7890)
            self._check_and_terminate_process(self, 9090)

            client = f'{os.getcwd()}/mihomo'
            self._process = subprocess.Popen([f"{client}", '-f', './sub.yaml'], text=True)
            logger.info("启动mihomo客户端")
            time.sleep(30)
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)

    def _before_stop_client(self):
        pass

    def stop_client(self):
        self._before_stop_client()
        if self._process is not None:
            self._process.send_signal(signal.SIGINT)
            self._check_and_terminate_process(self, 7890)
            self._check_and_terminate_process(self, 9090)
            # 等待进程退出
            self._process.wait()
            self._process = None      
            logger.info("Client Stop!")

    @staticmethod
    def _check_and_terminate_process(self, port):
        try:
            # 查找占用指定端口的进程
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    pid = conn.pid
                    process = psutil.Process(pid)
                    process.terminate()
                    logger.info(f"端口{port}占用已解除，PID：{pid}")
        except Exception as e:
            logger.error(f"错误： {str(e)}")


if __name__ == '__main__':
    clash = Clash()
    clash.start_client()
    clash.stop_client()
