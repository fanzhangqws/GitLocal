from sqlalchemy import Column, String, Integer, Sequence, Date
from base import Base

class ServiceRequest(Base):
    __tablename__ = 'ServiceRequest'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)

    op=Column(String(200))
    serialuserid=Column(String(200))
    customerid=Column(String(200))
    acc_nbr=Column(String(200))
    order_state=Column(String(200))
    is_that_day=Column(String(200))
    grid_name = Column(String(200))
    name=Column(String(200))
    address=Column(String(200))
    contact=Column(String(200))
    tel=Column(String(200))
    mobile=Column(String(200))
    location=Column(String(200))
    faulttype=Column(String(200))
    faultdetail = Column(String(200))
    other = Column(String(200))
    last_modify_time =Column(Date())
    errormsg = Column(String(200))    
    send_status = Column(String(200))
    succeed_status = Column(String(200))
    finish_status = Column(String(200))
    appl_date = Column(Date())
    send_date = Column(Date())
    return_date = Column(Date())
    
