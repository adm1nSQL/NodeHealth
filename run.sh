#!/bin/bash

# 检查 Python3 是否已安装
if ! command -v python3 &> /dev/null; then
    echo "未安装 Python3，请手动安装后再运行此脚本."
    exit 1
fi

# 检查 pip3 是否已安装，如果不存在则尝试安装
if ! command -v pip3 &> /dev/null; then
    echo "未安装 pip3，尝试安装..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# 检查 curl 是否已安装，如果不存在则尝试安装
if ! command -v curl &> /dev/null; then
    echo "未安装 curl，尝试安装..."
    sudo apt install -y curl
fi

echo "检查并安装依赖项..."
while read -r package; do
    if pip3 show "$package" &> /dev/null; then
        echo "$package 已安装"
    else
        echo "安装 $package..."
        pip3 install "$package"
    fi
done < requirements.txt

if [ -e "mihomo" ]; then
    echo "mihomo客户端文件已存在."
else
    echo "mihomo客户端文文件不存在，进行下载..."
    curl -O https://sub.183tk.tk/mihomo
    echo "mihomo客户端文下载完成."
fi

chmod +x mihomo
clear

show_menu() {
    while true; do     
        echo "************************************"
        echo "#        节点检测程序              #"
        echo "#                                  #"
        echo "#      TG频道 @fffffx2             #"
        echo "************************************"
        echo "菜单："
        echo "1. 运行程序"
        echo "2. 结束程序"
        echo "0. 退出"
        read -p "输入你的选择（0/1/2）：" choice

        case $choice in
            1)
                if [ -e "configs.json" ]; then
                    # 检查 configs.json 的值是否为空
                    if grep -q '"bot_token": ""' configs.json || grep -q '"chat_id": ""' configs.json || grep -q '"clash_api": ""' configs.json || grep -q '"hosting": ""' configs.json || grep -q '"airport_name": ""' configs.json || grep -q '"sub_url": ""' configs.json; then
                        echo "configs.json 中有值为空的字段，请修改 configs.json 然后重试"
                        exit 1
                    else
                        echo "启动节点检测程序并使用screen挂起..."
                        # 在后台运行程序
                        screen -S nodehealth -d -m python3 main.py
                        echo "节点检测程序已启动"
                        return
                    fi
                else
                    echo "未找到 configs.json 文件，请创建 configs.json 然后重试"
                    exit 1
                fi
                ;;
            2)
                echo "检查节点检测程序是否运行中..."
                if screen -list | grep -q "nodehealth"; then
                    screen -S nodehealth -X quit
                    echo "节点检测程序已终止"
                else
                    echo "节点检测程序当前未运行"
                fi
                return
                ;;
            0)
                exit 0
                ;;
            *)
                echo "无效选择，请输入 0、1 或 2"
                ;;
        esac
    done
}

show_menu
