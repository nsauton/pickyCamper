from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocale
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# write basemodels here
class IngredientBase(BaseModel):
    name: str

class MeasurementBase(BaseModel):
    ingredient: IngredientBase
    quantity: float
    unit: str

class RecipeBase(BaseModel):
    name: str
    meal: str
    instructions: str
    source: str
    category: str
    servingSize: float
    time: int
    effortRating: int
    picture: str
    dehydrate: bool
    measurements: List[MeasurementBase]


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

@app.post("/recipes")
async def add_recipe(recipe: RecipeBase, db: db_dependecy):
    #add the recipe
    db_recipe = models.Recipes(name = recipe.name, 
                               meal = recipe.meal,
                               instructions = recipe.instructions,
                               source = recipe.source,
                               category = recipe.category, 
                               servingSize = recipe.servingSize, 
                               time = recipe.time,
                               effortRating = recipe.effortRating, 
                               picture = recipe.picture, 
                               dehydrate = recipe.dehydrate)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for measurement in recipe.measurements:
        #check if ingredient already exists, if not add it
        db_ingredient = db.query(models.Ingredients).filter(models.Ingredients.name == measurement.ingredient.name).first()
        if not db_ingredient:
            db_ingredient = models.Ingredients(name = measurement.ingredient.name)
            db.add(db_ingredient)
            db.commit()
            db.refresh(db_ingredient)
            
        #add the measurements
        db_measurement = models.Measurements(quantity = measurement.quantity,
                                             unit = measurement.unit,
                                             recipeID = db_recipe.id, 
                                             ingredientID = db_ingredient.id)
        db.add(db_measurement)

    db.commit()

    return {"recipeID": db_recipe.id}
        
@app.get("/recipes/{recipeID}")
async def get_recipe(recipeID: int, db: db_dependecy):
    res = db.query(models.Recipes).filter(models.Recipes.id == recipeID).first()
    if not res:
        raise HTTPException(status_code=404, detail='Recipe not found')
    return res
