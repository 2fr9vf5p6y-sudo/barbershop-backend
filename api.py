from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Barbershop API")

categories = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4},
]


@app.get("/categories")
def get_categories():
    return categories


@app.get("/categories/{category_id}")
def get_category(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category
    return PlainTextResponse("Category not found", status_code=404)
