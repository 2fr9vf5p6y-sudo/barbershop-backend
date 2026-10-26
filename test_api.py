import unittest

from fastapi.testclient import TestClient

from api import app


class CategoryApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_category_list(self):
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        self.assertTrue(all({"id", "name", "servicesCount"} <= item.keys()
                            for item in response.json()))

    def test_existing_category(self):
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1, "name": "Стрижки и укладки", "servicesCount": 5
        })

    def test_not_found(self):
        response = self.client.get("/categories/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, "Category not found")

    def test_each_category_matches_list(self):
        categories = self.client.get("/categories").json()
        for category in categories:
            with self.subTest(category_id=category["id"]):
                response = self.client.get(f'/categories/{category["id"]}')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), category)


if __name__ == "__main__":
    unittest.main()
