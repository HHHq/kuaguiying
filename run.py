#!/usr/bin/python
# -*- coding: utf-8 -*
""" 收集用例，运行用例，生成测试报告的主程序"""
import os, unittest
from common.send_email import SendEmail
from common.send_report_to_dingtalk import send_to_dingtalk
from datetime import datetime
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from HTMLTestRunnerCN import HTMLTestRunner
from flask import Flask, send_file

logger = MidWare.logger
# test目录的路径
case_path = os.path.join(config.root_path, "test")
# reports目录的路径
report_path = os.path.join(config.root_path, "reports")
loader = unittest.TestLoader()
logger.info("开始收集测试集")
# 收集test目录下所有test开头的模块作为测试集
suite = loader.discover(case_path)
suites = unittest.TestSuite(suite)
# 测试报告文件名格式
ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
report_filename = 'report-{}.html'.format(ts)
# 测试报告文件路径
report_path = os.path.join(report_path, report_filename)

logger.info("开始运行测试用例")
with open(report_path, mode='wb') as f:
    runner = HTMLTestRunner(f, title='跨规盈接口测试报告', description='以下是接口自动化测试报告，请查收!')
    runner.run(suites)
logger.info("测试用例run完毕")

# 163邮箱代发邮件
email_handler = SendEmail(smtpserver=read_yaml(config.yaml_path)["authorize_info"]["smtpserver"],
                          user=read_yaml(config.yaml_path)["authorize_info"]["user"],
                          password=read_yaml(config.yaml_path)["authorize_info"]["password"],
                          sender=read_yaml(config.yaml_path)["authorize_info"]["sender"],
                          receiver=read_yaml(config.yaml_path)["authorize_info"]["receiver"],
                          report_path=report_path)
email_handler.send_email()

#  把报告挂在flask服务上
app = Flask(__name__)


@app.route('/')
def index():
    return send_file(report_path, mimetype='text/html')


# 发送报告至钉钉群聊
send_to_dingtalk(webhook_url=read_yaml(config.yaml_path)["webhook_url"], domain_url=read_yaml(config.yaml_path)["domain_url"])

app.run(host='0.0.0.0')
