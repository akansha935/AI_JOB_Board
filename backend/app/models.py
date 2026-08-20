from sqlalchemy import Column, String, Text, Integer, ARRAY
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    source = Column(String)
    description = Column(Text)
    min_experience = Column(Integer, nullable=True)
    max_experience = Column(Integer, nullable=True)
    domain = Column(String, nullable=True)
    skills_raw = Column(Text, nullable=True)
    posted_at = Column(String, nullable=True)
    apply_url = Column(String, nullable=True)

    ai_tags = Column(ARRAY(String), nullable=True)
    ai_role_category = Column(String, nullable=True)
    ai_experience_level = Column(String, nullable=True)
