from pydantic import BaseModel, Field, field_validator


class ServiceCreate(BaseModel):
    categoryId: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=100)
    desc: str = Field(min_length=1, max_length=100)
    duration: int = Field(ge=30, le=180)
    price: float = Field(gt=0, allow_inf_nan=False)

    @field_validator("title", "desc")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value
