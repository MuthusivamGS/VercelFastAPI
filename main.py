from fastapi import FastAPI
from db.database import Base, engine
from api.routes import router
from models import image
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)