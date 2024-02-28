import json, unittest
from config import config
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.yaml_handler import read_yaml
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_查看活动专区详情")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserActivityDetail(unittest.TestCase):
    '''用户端-用户端_查看活动专区详情'''

    def setUp(self):
        self.user_token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    # @unittest.skip("1111")
    def test_user_activityDetail(self, info):
        # seckillActivityId 写入json
        with open(config.json_path, "r+") as f:
            test_info = json.load(f)
            test_info["seckillActivityId"] =138
        with open(config.json_path, "w+") as f:
            json.dump(test_info, f)

        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)
        # 替换json文件product_id
        if "#seckillActivityId#" in info["data"]:
            with open(config.json_path, "r+") as f:
                seckillActivityId = json.load(f)["seckillActivityId"]
            info["data"] = info["data"].replace("#seckillActivityId#", str(seckillActivityId))

        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    )
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])

            logger.info("用户端_查看活动专区详情_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_查看活动专区详情_测试用例id_{}不通过".format(info["case_id"]))
            raise e



