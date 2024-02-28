import json, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_登录")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserLogin(unittest.TestCase):
    '''用户端-登录模块'''

    @ddt.data(*excel_data)
    def test_user_login(self, info):
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    )
        if info["case_id"] == 4:

            try:
                self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
                self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"][:11])

                logger.info("用户端_登录-测试用例id_{}通过".format(info["case_id"]))
            except Exception as e:
                logger.error("用户端_登录-测试用例id_测试用例id_{}不通过".format(info["case_id"]))
                raise e
        else:
            try:
                self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
                self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])

                logger.info("用户端_登录-测试用例id_{}通过".format(info["case_id"]))
            except Exception as e:
                logger.error("用户端_登录-测试用例id_测试用例id_{}不通过".format(info["case_id"]))
                raise e
