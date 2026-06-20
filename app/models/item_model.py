from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False) 
    status = Column(String, default="Pendente")
    created_at = Column(DateTime, default=datetime.utcnow)

    
# pra fazer rodar: uvicorn app.main:app --host 0.0.0.0 --port $PORT
