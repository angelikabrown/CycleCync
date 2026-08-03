from app.routers import daily_checkins
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.models.daily_check_in import DailyCheckIn
from app.routers import users

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the users router
app.include_router(users.router)
app.include_router(daily_checkins.router)

@app.get("/")
def root():
    return {"message": "CycleCync API is running!"}

