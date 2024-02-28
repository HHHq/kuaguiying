import requests


def send_to_dingtalk(webhook_url, domain_url):
    message = {
        "msgtype": "link",
        "link": {
            "title": "接口自动化报告地址",
            "text": "点击打开报告地址",
            "messageUrl": domain_url
        }
    }
    response = requests.post(webhook_url, json=message)
    # if response.status_code == 200:
    #     print("消息发送成功")
    # else:
    #     print("消息发送失败")



