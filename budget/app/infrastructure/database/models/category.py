from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(Integer, nullable=False)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    favicon = Column(String(100), nullable=True)
    children = relationship("Category", backref="parent", remote_side=[id], cascade='all')
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, type={self.type}, parent_category_id={self.parent_category_id})>"
    
