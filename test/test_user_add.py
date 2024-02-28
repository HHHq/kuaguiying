import json, ddt, unittest, datetime
from config import config
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.yaml_handler import read_yaml
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_添加购物车")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserAdd(unittest.TestCase):
    '''用户端-添加购物车模块'''

    def setUp(self):
        # 调用登录接口获取token
        self.user_token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    def test_user_add(self, info):
        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)
        # 从json文件中拿skuid
        try:
            with open(config.json_path, "r+") as f:
                skuid = json.load(f)["sku_id"]
        except Exception as e:
            logger.info("读取不了sku_id")

        # 动态替换excel中的 #skuid#
        if "#skuid#" in info["data"]:
            info["data"] = info["data"].replace("#skuid#", str(skuid))
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"])
                    )
        # 拿到 cartItemId 写入json
        if rsp["code"] == 200:
            with open(config.json_path, "r+") as f:
                product_info = json.load(f)
                product_info["cartItemId"] = rsp["data"]["id"]
            with open(config.json_path, "w+") as f:
                json.dump(product_info, f)

        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])
            logger.info("用户端_添加购物车_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_添加购物车_测试用例id_{}不通过".format(info["case_id"]))
            raise e
