import json, ddt, unittest, datetime
from config import config
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.yaml_handler import read_yaml
from common.db_handler import DbHandler
from common import ddt

excel_data = ExcelHandler(config.excel_path).read_sheet("管理端_添加商品")
request_url = read_yaml(config.yaml_path)["env_admin"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestAdminAddProduct(unittest.TestCase):
    '''管理端-添加商品模块'''

    @classmethod
    def setUpClass(cls) -> None:
        cls.product_id = []
        cls.admin_token = MidWare().get_admin_token()
        cls.db = DbHandler(host='rm-uf6s7pdj1829869iu.mysql.rds.aliyuncs.com',
                           user='user_vat_mall',
                           password='X0FcdHU8Rt_HSU5D8XR5bbK2',
                           port=3306,
                           database="vat_mall"
                           )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.close()

    @ddt.data(*excel_data)
    # @unittest.skip("111111")
    def test_admin_addproduct(self, info):
        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.admin_token)
        if "#time#" in info["data"]:
            info["data"] = info["data"].replace("#time#", str(datetime.datetime.now()))

        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    )
        if rsp["code"] == 200:
            self.product_id.append(rsp["data"])

            # product_id 关联查询找到skuid
            sku_id = self.db.query("select id from sku where product_id={}".format(self.product_id[0]))[0]
            # 商品id 和 skuid 写入json
            product_info = {"product_id": self.product_id[0], "sku_id": sku_id}
            with open(config.json_path, "w+") as f:
                json.dump(product_info, f)

        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])
            logger.info("管理端_添加商品-测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("管理端_添加商品-测试用例id_测试用例id_{}不通过".format(info["case_id"]))
            raise e
