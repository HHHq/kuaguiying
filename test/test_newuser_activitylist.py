import json, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common import ddt, db_handler

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_购买服务_新人活动专区列表")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestNewUserActivityList(unittest.TestCase):
    '''用户端-购买服务-新人活动专区列表'''

    def setUp(self):
        # 生成新的手机号
        self.new_phone = MidWare().generate_phone_number()
        # 新的手机号,发送验证码
        visit("post",
              url=request_url + "/api/user/verCode/sendCode",
              json={"phone": self.new_phone, "type": "register"},
              headers={"Content-Type": "application/json"})
        # 新用戶注册拿access_token
        rsp = visit("post",
                    url=request_url + "/api/user/register",
                    json={"username": self.new_phone, "verCode": self.new_phone[-6:]}
                    )
        self.new_user_accesstoken = rsp["data"]["access_token"]
        # 旧用户登录拿access_token
        self.token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    # @unittest.skip("111")
    def test_newuser_activitylist(self, info):
        if info["title"] == "新人活动-新用户":
            if "#token#" in info["header"]:
                info["header"] = info["header"].replace("#token#", self.new_user_accesstoken)
                rsp = visit(method=info["method"],
                            url=request_url + info["url"],
                            headers=json.loads(info["header"]),
                            )
                try:
                    # 新用户data里面活动数据不为空
                    self.assertTrue(rsp["data"] is not None)
                    logger.info("用户端_购买服务_新人活动专区列表_测试用例id_{}通过".format(info["case_id"]))

                except Exception as e:
                    logger.error("用户端_购买服务_新人活动专区列表_测试用例id_{}不通过".format(info["case_id"]))
                    raise e

        # 旧用户走这里的逻辑
        else:
            if "#token#" in info["header"]:
                info["header"] = info["header"].replace("#token#", self.token)
                rsp = visit(method=info["method"],
                            url=request_url + info["url"],
                            headers=json.loads(info["header"]))
                # 旧用户data里面没有活动数据为空
                try:
                    self.assertTrue(rsp["data"] is None)
                    logger.info("用户端_购买服务_新人活动专区列表_测试用例id_{}通过".format(info["case_id"]))
                except Exception as e:
                    logger.error("用户端_购买服务_新人活动专区列表_测试用例id_{}不通过".format(info["case_id"]))
                    raise e
