import unittest

from fastapi.testclient import TestClient
from sqlalchemy import select

from api import app
from database import Master, SessionLocal


class MastersApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_master_model_and_table(self):
        self.assertEqual(Master.__tablename__, "masters")
        with SessionLocal() as session:
            self.assertGreaterEqual(len(session.scalars(select(Master)).all()), 2)

    def test_list_masters(self):
        response = self.client.get("/masters")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[:2], [
            {"id": 1, "name": "Анна", "specialization": "Парикмахер"},
            {"id": 2, "name": "Мария", "specialization": "Визажист"},
        ])

    def test_filter_by_specialization(self):
        response = self.client.get("/masters", params={"specialization": "Парикмахер"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": 1, "name": "Анна", "specialization": "Парикмахер"}
        ])
        self.assertEqual(self.client.get("/masters?specialization=Неизвестная").json(), [])

    def test_get_master_by_id(self):
        response = self.client.get("/masters/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 2, "name": "Мария", "specialization": "Визажист"
        })

    def test_missing_master(self):
        response = self.client.get("/masters/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
