from pydantic import BaseModel



class UserBase(BaseModel):
    email: str
    username: str
    password: str
    class Config:
        orm_mode = True
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str
    email: str
    
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str