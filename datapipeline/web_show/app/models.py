from sqlalchemy import Column, Integer, String, ForeignKey, Date,Sequence, create_engine
from flask_appbuilder.models.decorators import renders
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

ora = create_engine('oracle://xxx:xxx@(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)\
                        (HOST = x.x.x.x)(PORT = xxx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))')

class OrderStatusTable(Model):
    __bind_key__ = 'service_change'
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

    @property
    def work_area(self):
        conn = ora.connect()
        sql = """
        select area.name 装机公司
   from cdcuser.so@cdcoss        so,
        cdcuser.wo@cdcoss        wo,
        cdcuser.work_area@cdcoss area
  where so.EXT_SO_NBR = :so
    and so.so_nbr = wo.so_nbr
    and wo.step_id = 'SP0701A'
    and wo.WORK_AREA_ID = area.WORK_AREA_ID and rownum=1
    """
        data = conn.execute(sql, so=self.serialuserid).fetchone()
        if data:
            return data[0]
        else:
            return 0



class service_request(Model):
    __bind_key__ = 'service_request'
    __tablename__ = 'ServiceRequest'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    op=Column(String(200))
    serialuserid=Column(String(200))
    customerid=Column(String(200))
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

