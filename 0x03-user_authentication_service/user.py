#!/usr/bin/env python3
"""User model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import Optional

Base = declarative_base()


class User(Base):
    """User model definition"""
    __tablename__: str = 'users'
    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
    session_id: Optional[Column] = Column(String, nullable=True)
    reset_token: Optional[Column] = Column(String, nullable=True)
