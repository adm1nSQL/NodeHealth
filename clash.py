import os
import subprocess
import sys
import time
import signal
from function import *


class Clash(object):
    def __init__(self):
        self._process = None
        self._pid = None

    def start_client(self):
        try:
            client = f'{os.getcwd()}/mihomo'
            self._process = subprocess.Popen([f"{client}", '-f', './sub.yaml'], text=True)
            logger.info("启动mihomo客户端")
            time.sleep(5)
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)

    def _before_stop_client(self):
        pass

    def stop_client(self):
        self._before_stop_client()
        if self._process is not None:
            self._process.send_signal(signal.SIGINT)
            # 等待进程退出
            self._process.wait()
            self._process = None
            logger.info("Client Stop!")


if __name__ == '__main__':
    pass
    # clash = Clash()
    # clash.start_client()
    # time.sleep(10)
    # clash.stop_client()
