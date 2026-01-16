from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.sql.expression import text

from app.core.database import Base



#======= USER model ================#

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))