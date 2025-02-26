from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(255))
    assigned_agent_id = Column(Integer, ForeignKey("users.id"))
