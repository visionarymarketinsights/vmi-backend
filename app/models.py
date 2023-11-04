from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    description = Column(String)
    toc = Column(String)
    highlights = Column(String)
    methodology = Column(String)
    meta_title = Column(String)
    meta_desc = Column(String)
    meta_keyword = Column(String)
    pages = Column(String)
    created_date = Column(String)
