import json, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common import ddt, db_handler

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_购买服务_列表")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserList(unittest.TestCase):
    '''用户端-购买服务-列表模块'''

    def setUp(self):
        self.user_token = MidWare().get_user_token()

    @ddt.data(*excel_data)
    # @unittest.skip("111")
    def test_user_list(self, info):
        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    )
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])
            if info["title"] == "知识产权-美国":
                # 查询数据库，知识产权-美国的商品数量 与 rsp["data"]的长度做断言
                query_sql = "select count(1) from product  where country_id = 15 and first_category_id = 33 and country_name = '美国' and status = 2 and product_user_visible = 1 and is_deleted = 0"
                db = db_handler.DbHandler(host='rm-uf6s7pdj1829869iu.mysql.rds.aliyuncs.com',
                                          user='user_vat_mall',
                                          password='X0FcdHU8Rt_HSU5D8XR5bbK2',
                                          port=3306,
                                          database="vat_mall"
                                          )
                count = db.query(query_sql)[0]
                try:
                    self.assertTrue(count == len(rsp["data"]))
                except Exception as e:
                    logger.error("数据库查询数量与接口返回的长度不一致")
                    raise e

            logger.info("用户端_购买服务_列表_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_购买服务_列表_测试用例id_{}不通过".format(info["case_id"]))
            raise e
