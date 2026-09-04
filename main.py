#main.py
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints (JSON responses)
@app.post("/api/users/", response_model=schemas.UserResponse)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/api/users/", response_model=list[schemas.UserResponse])
def read_users_api(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.get("/api/users/{user_id}", response_model=schemas.UserResponse)
def read_user_api(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/users/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.put("/api/users/{user_id}", response_model=schemas.UserResponse)
def update_user_api(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# HTML Template Route - Single Page Application
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")