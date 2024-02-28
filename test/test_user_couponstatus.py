import json, unittest
from config import config
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.yaml_handler import read_yaml
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_用户优惠券状态数量统计")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserCouponStatusStat(unittest.TestCase):
    '''用户端_用户优惠券状态数量统计'''

    def setUp(self):
        self.user_token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    def test_user_couponstatusstat(self, info):

        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)

        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    # json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    )
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])

            logger.info("用户端_用户优惠券状态数量统计_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_用户优惠券状态数量统计_测试用例id_{}不通过".format(info["case_id"]))
            raise e



