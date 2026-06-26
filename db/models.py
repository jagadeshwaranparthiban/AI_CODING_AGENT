from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Integer

from .database import Base


class Execution(Base):

    __tablename__ = "executions"
    id = Column(String, primary_key=True)
    prompt = Column(Text)
    generated_code = Column(Text)
    output = Column(Text)
    error = Column(Text)
    iteration = Column(Integer)