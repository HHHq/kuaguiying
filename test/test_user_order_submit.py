import json, unittest, requests
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.yaml_handler import read_yaml
from config import config
from common import ddt, db_handler

excel_data = ExcelHandler(config.excel_path).read_sheet("用户端_提交订单")
request_url = read_yaml(config.yaml_path)["env_user"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestUserOrderSubmit(unittest.TestCase):
    '''用户端-提交订单模块'''

    def setUp(self):
        # 调用登录接口/订单接口  获取token
        self.user_token = MidWare().get_user_token()
        reponse = requests.post(url=read_yaml(config.yaml_path)["env_user"]["url"] + "/api/mall/order/token",
                                headers={"Content-Type": "application/json", "Authorization": self.user_token})
        self.order_token = reponse.json()["data"]

        # 链接数据库
        self.db = db_handler.DbHandler(host='rm-uf6s7pdj1829869iu.mysql.rds.aliyuncs.com',
                                       user='user_vat_mall',
                                       password='X0FcdHU8Rt_HSU5D8XR5bbK2',
                                       port=3306,
                                       database="vat_mall"
                                       )

    def tearDown(self):
        self.db.close()

    @ddt.data(*excel_data)
    # @unittest.skip("11111")
    def test_user_order_submit(self, info):

        # 从json文件中拿skuid/productId/cartItemId
        with open(config.json_path, "r+") as f:
            data = json.load(f)
            skuid = data["sku_id"]
            productId = data["product_id"]
            cartItemId = data["cartItemId"]

        # 动态替换excel中的 token/skuid/product_id/cartItemId
        if "#token#" in info["header"]:
            info["header"] = info["header"].replace("#token#", self.user_token)
        if "#skuId#" in info["data"]:
            info["data"] = info["data"].replace("#skuId#", str(skuid))
        if "#productId#" in info["data"]:
            info["data"] = info["data"].replace("#productId#", str(productId))
        if "#cartItemId#" in info["data"]:
            info["data"] = info["data"].replace("#cartItemId#", str(cartItemId))
        if "#order_token#" in info["data"]:
            info["data"] = info["data"].replace("#order_token#", self.order_token)
        logger.info("提交订单的入参为!!!!!!!!!!!!{}".format(info["data"]))
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"])
                    )
        logger.info("提交订单的返回参数为!!!!!!!!!!!!{}".format(rsp))

        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["msg"] == rsp["msg"])
            logger.info("用户端_提交订单_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("用户端_提交订单_测试用例id_{}不通过".format(info["case_id"]))
            raise e
