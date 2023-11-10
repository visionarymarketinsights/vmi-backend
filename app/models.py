from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    summary = Column(String)
    description = Column(String)
    toc = Column(String)
    highlights = Column(String)
    methodology = Column(String)
    faqs = Column(String)
    meta_title = Column(String)
    meta_desc = Column(String)
    meta_keyword = Column(String)
    pages = Column(String)
    created_date = Column(String)
    


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, nullable=False)
    abr = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=False)


class ReportImage(Base):
    __tablename__ = "report_image"

    id = Column(Integer, primary_key=True, nullable=False)
    img_name = Column(String, nullable=False)
    img_file = Column(String, nullable=False)

class PressRelease(Base):
    __tablename__ = "press_release"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    meta_title = Column(String)
    meta_desc = Column(String)
    meta_keyword = Column(String)
    created_date = Column(String)