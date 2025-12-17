from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocale
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# write basemodels here

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()
    

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello world! this is the pickyCamper API"}