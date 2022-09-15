from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, default=False)

    class Config:
        orm_mode = True
