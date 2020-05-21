from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db',echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(255))
    fullname = Column(String)
    password = Column(String)
    age = Column(Integer)

    def __init__(self,name, fullname, password, age):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.age = age

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
# vasia = User('vasia','Vasiliy Pupkin','Vasia2000',30)
# session.add(vasia)
# session.add_all([User("kolia", "Cool Kolian[S.A.]","kolia$$$", 28),
#                     User("zina", "Zina Korzina", "zk18", 54)])

for instance in session.query(User).filter(User.age > 29):
    print(instance.name, instance.password)

session.commit()
session.close()