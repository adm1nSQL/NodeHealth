# NodeHealth

一个用 Telegram bot api 来对订阅节点进行定时检测的程序，基于[mihomo(clash meta)]([https://t.me/BotFather](https://github.com/MetaCubeX/mihomo/releases))

## 快速开始

* 从 [@BotFather](https://t.me/BotFather) 那里创建一个机器人，获得该机器人的bot_token，应形如：

    bot_token = "xxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxx"

    这步不会请Google。
* 动动你的小手拉取本项目的源码
```shell
apt install -y git && git clone https://github.com/adm1nSQL/Sub_Manger.git && cd Sub_Manger
```

* 安装依赖 Python 3.6 以上



赋权run.sh

```
chmod +x run.sh
```

* 运行

首次运行需在configs.json传入参数：
```shell
bot_token：你的机器人token
chat_id： 消息推送的个人或群ID
clash_api： 默认设置的9090，需根据你的实际配置文件修改，clash配置文件中external-controller指定的端口
hosting：测试后端名称，例如：北京电信
airport_name：你的机场名称，主要为消息推送中的输出
sub_url：你的clash订阅链接
```

一键启动并使用screen挂起
```shell
./run.sh
```


