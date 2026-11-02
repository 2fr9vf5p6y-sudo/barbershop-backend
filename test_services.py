import unittest
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from api import app
from database import Service, SessionLocal
from schemas import ServiceCreate


class ServicesApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.created_ids = []

    def tearDown(self):
        with SessionLocal() as db:
            for service_id in self.created_ids:
                item = db.get(Service, service_id)
                if item is not None:
                    db.delete(item)
            db.commit()

    def test_valid_service_is_saved_in_sqlite(self):
        payload = {
            "categoryId": 3,
            "title": "Наращивание ресниц",
            "desc": "Огромные ресницы уже через 30 минут",
            "duration": 30,
            "price": 1500.00,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.created_ids.append(result["id"])
        self.assertEqual(result["title"], payload["title"])
        with SessionLocal() as db:
            stored = db.get(Service, result["id"])
            self.assertIsNotNone(stored)
            self.assertEqual(stored.category_id, 3)
            self.assertEqual(stored.duration, 30)

    def test_price_as_text_returns_422(self):
        response = self.client.post("/services", json={
            "categoryId": 3, "title": "Наращивание ресниц",
            "desc": "Огромные ресницы уже через 30 минут",
            "duration": 30, "price": "бесплатно",
        })
        self.assertEqual(response.status_code, 422)

    def test_invalid_values_return_422(self):
        response = self.client.post("/services", json={
            "categoryId": 3, "title": "Наращивание ресниц",
            "desc": "", "duration": 0, "price": -1500.00,
        })
        self.assertEqual(response.status_code, 422)

    def test_boundaries_and_blank_strings(self):
        valid = dict(categoryId=1, title="Услуга", desc="Описание", duration=180, price=1)
        self.assertIsNotNone(ServiceCreate(**valid))
        for field, value in [("title", "  "), ("desc", " "), ("title", "a" * 101),
                             ("duration", 29), ("duration", 181), ("price", 0)]:
            with self.subTest(field=field, value=value):
                invalid = {**valid, field: value}
                self.assertEqual(self.client.post("/services", json=invalid).status_code, 422)

    def test_unknown_category_returns_404(self):
        response = self.client.post("/services", json={
            "categoryId": 999, "title": "Услуга", "desc": "Описание",
            "duration": 30, "price": 100,
        })
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
