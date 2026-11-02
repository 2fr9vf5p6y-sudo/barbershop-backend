from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Master, Service, get_db
from schemas import ServiceCreate

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


@app.post("/services", status_code=201)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    if not any(category["id"] == service.categoryId for category in categories):
        raise HTTPException(status_code=404, detail="Category not found")

    new_service = Service(
        category_id=service.categoryId,
        title=service.title,
        desc=service.desc,
        duration=service.duration,
        price=service.price,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return {
        "id": new_service.id,
        "categoryId": new_service.category_id,
        "title": new_service.title,
        "desc": new_service.desc,
        "duration": new_service.duration,
        "price": new_service.price,
    }
