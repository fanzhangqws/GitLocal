from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('oracle://xxx:xxx@(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)\
                        (HOST = x.x.x.x)(PORT = xxxx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))')

Session = sessionmaker(bind=engine)

Base = declarative_base()