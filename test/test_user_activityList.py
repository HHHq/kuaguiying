import json, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_查看活动专区列表")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserList(unittest.TestCase):
    '''用户端-活动专区-列表模块'''

    def setUp(self):
        self.user_token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    # @unittest.skip("11111")
    def test_user_list(self, info):
        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    headers=json.loads(info["header"]),
                    )
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])

            logger.info("用户端_活动专区_列表_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_活动专区_列表_测试用例id_{}不通过".format(info["case_id"]))
            raise e
