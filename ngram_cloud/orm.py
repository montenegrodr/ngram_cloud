import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
host = os.getenv('HOST', '')
passwd = os.getenv('DB_PASSWD', '')
user = os.getenv('DB_USER', 'root')
database = os.getenv('DB_NAME', 'bigrams')


class Vocab(Base):
    __tablename__ = 'vocab'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    hits = Column(Integer)


class Association(Base):
    __tablename__ = 'associations'

    id = Column(Integer, primary_key=True)
    word1_id = Column(Integer)
    word2_id = Column(Integer)
    hits = Column(Integer)
    rate = Column(Integer)
    solved = Column(Boolean)


class Database(object):
    def __init__(self, **kwargs):
        self.connection_string = kwargs['con_str']
        self.eng = self._create_eng()
        self.session = None

        Base.metadata.bind = self.eng
        Base.metadata.create_all()

    def open_session(self):
        self.session = self._create_session()

    def close_session(self):
        if self.session:
            self.session.close()

    def _create_eng(self):
        return create_engine(self.connection_string)

    def _create_session(self):
        return sessionmaker(bind=self.eng)()

    def list_vocab(self):
        return self.session.query(Vocab).all()


class DataController(object):
    def __init__(self):
        con_str = f'mysql://{user}:{passwd}@{host}/{database}'
        self.db = Database(con_str=con_str)

    def __enter__(self):
        self.db.open_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close_session()


class VocabWord:
    def __init__(self, word, occurrences):
        self.word = word
        self.occurrences = occurrences


class VocabController(DataController):
    def list(self):
        return [VocabWord(v.word, v.hits)
                for v in self.db.list_vocab()]
