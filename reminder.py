from sqlalchemy import Column, Text, Integer, Date, create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from datetime import datetime, date, timedelta


class Base(DeclarativeBase):
    ...


class RemList(Base):
    __tablename__ = "remlist"

    id = Column(Integer, nullable=False, primary_key=True)
    mov_id = Column(Text, nullable=False)
    mov_tittle = Column(Text, nullable=False)
    release_date = Column(Date, nullable=False)
    remember = Column(Integer, nullable=False)


engine = create_engine("sqlite:///remind.db")
factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
session = scoped_session(factory)

Base.metadata.create_all(bind=engine)


# Add remind object
def set_data(mov_id: str, release_date: str, mov_tittle: str):
    today_date = date.today()
    trigger = 3
    if datetime.strptime(release_date, '%Y-%m-%d').date() >= today_date + timedelta(days=7):
        trigger = 3
    elif datetime.strptime(release_date, '%Y-%m-%d').date() >= today_date + timedelta(days=3):
        trigger = 2
    elif datetime.strptime(release_date, '%Y-%m-%d').date() >= today_date:
        trigger = 1
    data = RemList(mov_id=mov_id,
                   mov_tittle=mov_tittle,
                   release_date=datetime.strptime(release_date, '%Y-%m-%d'),
                   remember=trigger)
    session.add(data)
    session.commit()


# Get remind list
def get_list():
    return session.query(RemList).all()


# Checker for remind activator
def check_date(release_date: str, mov_id: str):
    if datetime.strptime(release_date.replace('\\', ''), '%Y-%m-%d') > datetime.today() and not session.query(RemList)\
            .filter_by(mov_id=mov_id).first():
        return True
    else:
        return False
