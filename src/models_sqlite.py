from sqlalchemy import Column, Integer, String, Boolean
from sqlite import Base, engine

class User(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    mail_enabled = Column(Boolean, default=False) 
    destination_email = Column(String, nullable=True, default=None)  
    
Base.metadata.create_all(bind=engine)
