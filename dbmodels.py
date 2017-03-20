import os
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Offices(Base):
    __tablename__ = "Offices"
    office_id = Column(Integer)
    office_name = Column(String(25), primary_key=True)
    room_capacity = Column(Integer)


class LivingSpaces(Base):
    __tablename__ = "LivingSpaces"
    livingspace_id = Column(Integer, primary_key=True)
    livingspace_name = Column(String(25))
    room_capacity = Column(Integer)


class Fellows(Base):
    __tablename__ = "Fellows"
    fellow_id = Column(Integer, primary_key=True)
    fellow_name = Column(String(25))
    person_type = Column(String(25))
    wants_space = Column(String(5))


class Staff(Base):
    __tablename__ = "Staff"
    staff_id = Column(Integer, primary_key=True)
    staff_name = Column(String(25))
    person_type = Column(String(25))


class Allocated(Base):
    __tablename__ = "Allocated_fellows"
    livingspace_name = Column(String(25), primary_key=True)
    allocated_fellows = Column(String(50))


class Unallocated(Base):
    __tablename__ = "Unallocated_fellows"
    fellow_name = Column(String(50), primary_key=True)
    person_type = Column(String(10))
    wants_space = Column(String(5))


def create_db(dbname):
    db_dir = "models/"
    engine = create_engine('sqlite:///' + db_dir + dbname + '.db')
    return Base.metadata.create_all(engine)
