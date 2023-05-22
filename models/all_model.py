import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from typing import Union,List

Base = declarative_base()


class Base_model(Base):
    
    __abstract__ = True
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    def add_one(self,session:sqlalchemy.orm.session.Session):
        session.add(self)
        session.commit()

    def query_all(self,session:sqlalchemy.orm.session.Session):
        return session.query(self.__class__).all()

    def update_one(self,session:sqlalchemy.orm.session.Session):
        session.commit()
    def select_by_id(self,session:sqlalchemy.orm.session.Session,id):
        return session.get(self.__class__ ,id)
    def select_by_param(self,sesstion:sqlalchemy.orm.session.Session,**kwargs) -> Union[List,None]: 
        stmt = select(self.__class__)
        for k,v in kwargs.items():
            stmt = stmt.where(getattr(self.__class__,k)==v)
        return sesstion.scalars(stmt).all()
    def delete_by_id(self,session:sqlalchemy.orm.session.Session,id):
        session.delete(session.get(self.__class__ ,id))
        session.commit()

class Users(Base_model):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    tel = Column(String(20))
    role = Column(String(20))

    def __repr__(self):
        return f"uid= {self.uid}, username={self.username}, email={self.email}, password={self.password}, tel={self.tel}, role={self.role}\n"



class Reservation(Base_model):
    __tablename__ = 'reservation'
    rid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    username = Column(String(50),unique=True)
    tel = Column(String(20))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    status = Column(String(20))
    room_id = Column(Integer)
    room_name = Column(String(50))


class Room(Base_model):
    __tablename__ = 'room'
    rid = Column(Integer, primary_key=True)
    room_name = Column(String(50),unique=True)
    room_desc = Column(String(200))
    room_cover_pic = Column(String)
    room_inner_pic = Column(String)
    room_type = Column(String(20))

    def __repr__(self):
        return f"rid= {self.rid}, room_name={self.room_name}, room_desc={self.room_desc}, room_cover_pic={self.room_cover_pic}, room_inner_pic={self.room_inner_pic}, room_type={self.room_type}\n"

class Comment(Base_model):
    __tablename__ = 'comment'
    cid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    username = Column(String(50))
    comment_time = Column(DateTime)
    room_id = Column(Integer)
    comment = Column(String(200))


class BookMark(Base_model):
    __tablename__ = 'bookmark'
    bid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    room_id = Column(Integer)

engine = create_engine('mysql+pymysql://root:zzh0117.@113.31.110.212:3306/db9')



if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:zzh0117.@113.31.110.212:3306/db9')


    session = sessionmaker(bind=engine)
    session = session()
    # User = Users(username='zzh',email='123@gmail.com',password='123',tel='123',role='admin')
    # # res = User.query_all(session=session)
    # # User.add_one(session=session)
    # # res = User.query_all(session=session)[0]
    # # res.role = 'user'
    # # User.update_one(session=session)
    # res = User.select_by_id(session=session,id=3)    
    res = Users().select_by_param(session,username='zzh',role='admin')
    print(res)