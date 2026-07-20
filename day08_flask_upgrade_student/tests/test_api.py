import sys
from pathlib import Path
# 将项目根目录加入系统路径
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

import unittest
from app import app

class APITest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # 用例1：健康检测接口
    def test_health_200(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["ok"], True)

    # 用例2：未登录访问指标接口被拦截
    def test_metrics_no_login_redirect(self):
        res = self.client.get("/api/metrics")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.location)

    # 用例3：登录后指标接口正常返回数据
    def test_metrics_login_success(self):
        self.client.post("/login", data={"username": "student", "password": "day07"})
        res = self.client.get("/api/metrics")
        data = res.get_json()
        self.assertEqual(data["ok"], True)
        self.assertIsInstance(data["metrics"], list)

    # 用例4：Fashion品类筛选校验
    def test_category_filter_fashion(self):
        self.client.post("/login", data={"username": "student", "password": "day07"})
        all_data = self.client.get("/api/categories").get_json()["rows"]
        fashion_data = self.client.get("/api/categories?category=Fashion").get_json()["rows"]
        self.assertTrue(len(fashion_data) < len(all_data))

if __name__ == "__main__":
    unittest.main()