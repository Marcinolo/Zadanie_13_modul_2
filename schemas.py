from pydantic import BaseModel

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: str
    extra_data: str = None

class ContactOut(ContactCreate):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str