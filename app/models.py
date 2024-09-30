from sqlalchemy import Column, Float, Integer, String
from .database import Base

class Peak(Base):
    __tablename__ = "peaks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)