from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Master, get_db

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


def master_to_dict(master: Master) -> dict:
    return {
        "id": master.id,
        "name": master.name,
        "specialization": master.specialization,
    }


@app.get("/masters")
def get_masters(specialization: str | None = None, db: Session = Depends(get_db)):
    statement = select(Master).order_by(Master.id)
    if specialization is not None:
        statement = statement.where(Master.specialization == specialization)
    masters = db.scalars(statement).all()
    return [master_to_dict(master) for master in masters]


@app.get("/masters/{master_id}")
def get_master_by_id(master_id: int, db: Session = Depends(get_db)):
    master = db.get(Master, master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return master_to_dict(master)
