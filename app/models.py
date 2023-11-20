from sqlalchemy import Column, Integer, String, DateTime, func, Boolean # func는 mysql의 함수를 쓸 수 있게 해주는 녀석임
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.database import Base

class BaseMin:
  id = Column(Integer, primary_key=True, index=True)
  created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
  updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(),
                      onupdate=func.utc_timestamp())
  
class User(BaseMin, Base):
  __tablename__ = "user"
  
  email = Column(String(30), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  is_provider = Column(Boolean, default=True)
  items = relationship("TsItem", back_populates="owner")

class TsItem(BaseMin, Base):
  __tablename__ = "tsitem"

  dialect = Column(String(255), nullable=False)
  standard = Column(String(255), nullable=False)
  english = Column(String(255), nullable=False)
  owner_id = Column(Integer, ForeignKey("user.id"))

  owner = relationship("User", back_populates="items")