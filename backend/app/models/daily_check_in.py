from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base

class DailyCheckIn(Base):

    __tablename__ = "daily_check_ins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    cycle_day = Column(Integer, nullable=True)
    bbt = Column(Float, nullable=True)
    mood = Column(String(20), nullable=True)
    energy_level = Column(String(20), nullable=True)
    sleep_quality = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to the User model
    user = relationship("User", back_populates="daily_check_ins")