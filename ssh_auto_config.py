#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/12/18
# @Author  : 秋天的落寞

"""
批量配置交换机：
支持H3C设备
华为设备需将“device_type”的值改为 huawei，效果需自行验证
"""
import json
import re
import configparser
from loguru import logger
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException


def Login_device(IP, user, passwd):
    """
    登陆设备
    :param IP: 设备IP地址
    :param user: 用户名
    :param passwd: 密码
    :return: 登陆设备后的ssh长连接
    """
    try:
        device = {
            "device_type": "hp_comware",  # "hp_comware（H3C平台）", 网络设备类型
            "ip": IP,  # IP地址
            "username": user,  # 设备登陆账号
            "password": passwd  # 设备登陆密码
        }
        connect = ConnectHandler(**device)
        return connect
    except NetmikoAuthenticationException:
        logger.error(f"[-] {IP} 登陆认证失败，账号密码可能错误！")
    except NetmikoTimeoutException:
        logger.error(f"[-] 登陆超时，请确认({IP})网络是否正常或IP是否存在")
    except Exception as f:
        logger.error(f)


def Device_config(conn):
    """
    发送配置命令
    :param conn: Login_device函数的 connect
    :return:
    """
    try:
        output = conn.send_config_from_file(config_file="command_list.txt")
        print(output)
        # res = con.send_command("dis vlan")  # 打印发送1条配置
        # logger.info(res)
        save = conn.save_config()  # 保存配置
        if re.findall(r"successfully", save, re.I | re.M):
            logger.info("配置保存成功")
        else:
            logger.error("配置保存失败，请登陆设备确认是否保存！")
    except Exception as f:
        logger.error(f)


def user_passwd() -> list:
    """
    :return: 账号密码
    """
    try:
        users_file = configparser.ConfigParser()
        users_file.read("user_pass.ini")
        user = users_file.get("users", "user")
        passwd = users_file.get("users", "password")
        return [user, passwd]
    except Exception as f:
        logger.error(f)


def main():
    us_pa = user_passwd()
    with open('ip_list.txt', encoding='utf-8') as ip_list:
        for ip_add in ip_list:
            con = Login_device(ip_add.strip(), us_pa[0], us_pa[1])
            if con is not None:
                logger.info(f"[+] {ip_add.strip()} 登陆成功")
                Device_config(con)


if __name__ == "__main__":
    main()
