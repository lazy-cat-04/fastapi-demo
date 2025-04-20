from pydantic import BaseModel

# Schema để nhận dữ liệu từ client
class BookCreate(BaseModel):
    title: str
    description: str
    published_year: int

    class Config:
        orm_mode = True