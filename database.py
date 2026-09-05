# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://test_db_vbbs_user:nxCVgqlGbSwtblM0TlePi4SzN2xGSOdG@dpg-dadpp8id0e5s73dsq1mg-a.oregon-postgres.render.com/test_db_vbbs?sslmode=require"
)

engine = create_engine(DATABASE_URL)  # no connect_args here

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()