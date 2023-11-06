
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table
from fastapi import HTTPException
import models, schemas, database
import bcrypt

# method to delete the table "users"
def delete_users(db: Session):
    metadata = MetaData()
    table = Table("users", metadata, autoload_with=database.engine)
    table.drop(database.engine)
    metadata.create_all(database.engine)

# method to delete a single user in table "users"
def delete_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return "User deleted successfully"

# method to get a user from table "users" by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# method to get a user from table "users" by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# method to get all data from table "users" (max. 100 entries)
def get_users(db: Session, query: str = '', limit: int = 100):
    users = db.query(models.User).filter(models.User.username.like(f"%{query}%")).limit(limit).all()
    return [u.__dict__ for u in users]

# method to create a user into table "users"
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.User.from_orm(db_user).dict()

def update_user_by_username(db: Session, username: str, updated_data: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    if db_user:
        if updated_data.username:
            db_user.username = updated_data.username
        if updated_data.email:
            db_user.email = updated_data.email

        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
