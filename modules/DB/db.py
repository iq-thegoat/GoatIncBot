from sqlalchemy import create_engine,ForeignKey,Column,String,Integer,DateTime,LargeBinary,Boolean
from sqlalchemy.orm import declarative_base , sessionmaker
import datetime

global base 
base = declarative_base()
class Dbstruct:
    class users(base):
        __tablename__ = "users"
        id  = Column("user_id",Integer,primary_key=True)
        sub = Column("sub_type",String)
        end_sub= Column("end_sub",DateTime)

        def __init__(self,id:int,sub:str,end_sub:datetime.datetime.date):
            self.id = id
            self.sub=sub
            self.end_sub=end_sub
    
    class keys(base):
        __tablename__ = "keys"
        id  = Column("key_id",Integer,primary_key=True,autoincrement=True)
        key = Column("key",String)
        claimed_by = Column("claimed_by",Integer,default=None)
        sub = Column("sub_type",String)

        def __init__(self,key:str,sub:str):
            self.key=key
            self.sub=sub
    
    class combos(base):
        __tablename__ = "combos"
        id    = Column("id",Integer,autoincrement=True,primary_key=True)
        target= Column("target",String)
        file  = Column("file",LargeBinary)
        uploaded = Column("uploaded",Boolean,unique=False,default=False)
        upload_time=Column("upload_time",DateTime,default=datetime.datetime.utcnow)
    
        def __init__(self, target, file):
            self.target = target
            self.file = file
            self.upload_time = datetime.datetime.utcnow()

class BotDb:
    def __init__(self) -> None:
        engine = create_engine("sqlite:///database.db")
        base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
