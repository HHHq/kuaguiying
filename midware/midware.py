import requests, json, random

from common.log_output import log_output
from config import config
from common.yaml_handler import read_yaml


class MidWare():
    logger = log_output(filename=config.log_path)

    # 获取TOKEN
    def get_user_token(self):
        response = requests.post(
            url=read_yaml(config.yaml_path)["env_user"]["url"] + "/api/user/login",
            json={"username": read_yaml(config.yaml_path)["env_user"]["login_account"],
                  "password": read_yaml(config.yaml_path)["env_user"]["password"],
                  "loginType": "PASSWORD", "deviceType": 1},
            headers={"Content-Type": "application/json"}
        )
        user_token = response.json()["data"]["access_token"]
        return user_token

    def get_admin_token(self):
        response = requests.post(
            url=read_yaml(config.yaml_path)["env_admin"]["url"] + "/admin-api/system/login",
            json={"username": read_yaml(config.yaml_path)["env_admin"]["login_account"],
                  "password": read_yaml(config.yaml_path)["env_admin"]["password"],
                  "code": "666"},
            headers={"Content-Type": "application/json"}
        )
        admin_token = response.json()["token"]
        return "Bearer"+" "+admin_token

    # 拿提交订单入参token
    def get_order_token(self):
        reponse = requests.post(url=read_yaml(config.yaml_path)["env_user"]["url"] + "/api/mall/order/token",
                                headers={"Content-Type": "application/json", "Authorization": self.get_user_token()})
        return reponse.json()["data"]

    # 随机生成手机号
    def generate_phone_number(self):
        phone_number = '13'
        for _ in range(9):
            phone_number += str(random.randint(0, 9))
        return phone_number




