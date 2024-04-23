from sqlalchemy import Column, Integer, String, Boolean
from sqlite import Base, engine
from sqlalchemy.orm import mapped_column, Mapped

# class User(Base):
#     __tablename__ = "settings"
#
#     id = Column(Integer, primary_key=True)
#     mail_enabled = Column(Boolean, default=False)
#     destination_email = Column(String, nullable=True, default=None)
#


class User(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mail_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    destination_email: Mapped[str] = mapped_column(String, nullable=True, default=None)


Base.metadata.create_all(bind=engine)
