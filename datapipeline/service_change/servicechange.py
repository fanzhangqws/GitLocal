from sqlalchemy import Column, String, Integer, Sequence, Date
from base import Base

class ServiceChange(Base):
    __tablename__ = 'ServiceChange'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)

    op=Column(String(200))
    serialuserid=Column(String(200))
    customerid=Column(String(200))
    name=Column(String(200))
    cardtype=Column(String(200))
    idcardnum=Column(String(200))
    servicecode=Column(String(200))
    location=Column(String(200))
    ordertype=Column(String(200))
    parameters=Column(String(200))
    send_status = Column(String(200))
    succeed_status = Column(String(200))
    last_modify_time = Column(Date())
    CO = Column(String(200))
    errormsg = Column(String(4000))
    finish_status = Column(String(200))
    acc_nbr = Column(String(200))


class OrderStatusTable(Base):
    __tablename__ = 'OrderStatusTable'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)

    serialuserid=Column(String(200))
    location=Column(String(200))
    status = Column(String(200))
    CO = Column(String(200))
    errormsg = Column(String(200))
    appl_date = Column(Date())
    send_date = Column(Date())
    return_date = Column(Date())
    ordertype=Column(String(200))