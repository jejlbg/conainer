from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Create tables in the database based on the model definitions
models.Base.metadata.create_all(bind=engine)

# Create instance of FastAPI
app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# post method to delete table "users"
@app.post("/deleteUsers/")
def delete_users(db: Session = Depends(get_db)):
    db_delete_users = crud.delete_users(db)
    if db_delete_users:
        raise HTTPException(status_code=400, detail="Not Found")
    #return crud.get_users(db=db, skip=0, limit=100)

# post method to delete a single user from table "users" by id
@app.post("/deleteUser/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db_delete_user = crud.delete_user(db, username)
    if db_delete_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return {"message": "User deleted successfully", "status_code": 200}

# post method to create a user into table "users"
@app.post("/createUser/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/get_user/{username}")
async def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    return user

@app.put("/update_user/{username}")
async def update_user(username: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_by_username(db, username, user_update)
    return {"message": "User updated successfully"}

@app.get("/getUsers/", response_model=list[schemas.User])
def read_users(query: str = '', limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, query=query, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user