from sqlalchemy import Column, String, Text
from .database import Base
class Message(Base):
    __tablename__ = "messages"
    message_id = Column(String, primary_key=True, index=True) # Uniqueness
    from_msisdn = Column(String, nullable=False)
    to_msisdn = Column(String, nullable=False)
    ts = Column(String, nullable=False) # ISO-8601 string
    text = Column(Text, nullable=True)
    created_at = Column(String, nullable=False) # Server time 