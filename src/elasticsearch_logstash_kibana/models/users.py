from sqlalchemy import Column, Integer, String, Sequence
from elasticsearch_logstash_kibana.database.db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

Base.metadata.create_all(bind=engine)
