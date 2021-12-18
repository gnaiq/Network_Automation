# 网络自动化工具

#### 介绍
在工作中经常遇到需要对大量交换机进行配置，为解决重复且费时的批量配置工作，写了个简单的批量对交换机进行配置的工具。

#### 工具说明

工具共有两个txt文本和一个json：
1. ip_list.txt 用于存放IP地址
2. command_list.txt 用于存放配置命令
3. user_pass.json 用于存放账号密码（仅限1个）

#### 工具依赖库
安装工具所需库
```pip install -r requirements.txt```

#### 使用说明
文件全部放在同一个目录下，运行
>python ssh_auto_config.py
