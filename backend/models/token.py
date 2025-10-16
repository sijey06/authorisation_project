from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from settings.database import Base


class ActiveToken(Base):
    __tablename__ = "active_tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    token_value = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
