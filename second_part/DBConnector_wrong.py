import pandas as pd
import numpy as np
import sqlalchemy as sal
from collections import defaultdict
import datetime, time

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import func 
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


Base = declarative_base()

class Event_type(Base):
    __tablename__ = "Event_type"

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)

    def __repr__(self):
        return f"Event_type(event_id={self.event_id!r}, event_name={self.event_name!r})"

class Person(Base):
    __tablename__ = "Person"

    person_id = Column(Integer, primary_key=True)
    person_name = Column(String, nullable=False)
    person_photo_link = Column(String, nullable=False)
    person_model_link = Column(String, nullable=False)

    def __repr__(self):
        return f"Person(person_id={self.person_id!r}, person_name={self.person_name!r}, person_photo_link={self.person_photo_link!r}, \
            person_model_link={self.person_model_link!r})"


class Log(Base):
    __tablename__ = "Log"

    log_id = Column(Integer, primary_key=True)
    date = Column(sal.Date)
    time = Column(sal.Time)
    person_status = Column(String)
    event_id = Column(Integer, ForeignKey("Event_type.event_id"), nullable=False)

    def __repr__(self):
        return f"Log(log_id={self.log_id!r}, date={self.date!r}, time={self.time!r}, \
            status={self.person_status!r}, event_id={self.event_id!r})"


class Person_log(Base):
    __tablename__ = "Person_log"

    log_id = Column(Integer, ForeignKey("Log.log_id"),primary_key=True)
    person_id = Column(String,  ForeignKey("Person.person_id"), nullable=False)

    def __repr__(self):
        return f"Person_log(log_id={self.log_id!r}, person_id={self.person_id!r})"


class White_list(Base):
    __tablename__ = "White_list"

    person_id = Column(String,  ForeignKey("Person.person_id"), primary_key=True)

    def __repr__(self):
        return f"White_list(person_id={self.person_id!r})"

class DBConnector:
    def __init__(self):
        self.engine = None
        self.conn = None

    def connect_to_postgresql(self):
        print("Conection to database started...")
        USERNAME = 'julia'
        PASSWORD = 'qwerty322'
        HOST = '192.168.1.7'
        PORT = '5432'
        DATABASE_NAME = 'das_db'
        self.engine = sal.create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}')
        #('postgresql+psycopg2://user:password@host:port/database_name')
        self.conn = self.engine.connect()
        print("Connection established")
    
    def disconnect_from_db(self):
        self.conn.close()
        print("Connection with database was closed")


    def add_log_to_db(self, event_date, event_time,  event_type_id, 
                        visitor_status='Unknown', visitor_id=None):
        '''
            Event_type_id:  1 - door opened by system
                            2 - door opened by visitor
            visitor_status: 'White list', 'Unknown'
        '''

        # get last log id
        with Session(self.engine) as session:
            last_log_id = session.execute(sal.func.max(Log.log_id)).scalar()
        # create object
        log_1 = Log(log_id=last_log_id+1, date=event_date, time=event_time, 
                        event_id=event_type_id, person_status=visitor_status)
        # insert into db through session
        # one row
        with Session(self.engine) as session:
            session.add(log_1)
            session.commit()
        
        if visitor_id is not None:
            # connect person to event
            person_log_1 = Person_log(log_id=last_log_id+1,
                            person_id=visitor_id)
            session.add(person_log_1)
            session.commit()

    
    def get_whitelist(self):
        with Session(self.engine) as session:
            wl = session.query(Person, White_list).filter(Person.person_id==White_list.person_id).all()
            return wl


        
