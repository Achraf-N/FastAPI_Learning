from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
SQLALACHEMY_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
"""

SQLALACHEMY_URL = 'postgresql://postgres:00&Achraf&@localhost/fastApi'



engine = create_engine(SQLALACHEMY_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()