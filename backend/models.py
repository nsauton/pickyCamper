from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from database import Base

class Recipes(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default='')
    meal = Column(String, default='')
    instructions = Column(String, default='')
    source = Column(String, default='')
    category = Column(String, default='')
    servingSize = Column(Float)
    time = Column(Integer)
    effortRating = Column(Integer)
    picture = Column(String, default='') #url or filename
    dehydrate = Column(Boolean)

class Ingredients(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default='')

class Measurements(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True, index=True)
    recipeID = Column(Integer, ForeignKey("recipes.id"))
    ingredientID = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float, default=0.0)
    unit = Column(String, default='')
