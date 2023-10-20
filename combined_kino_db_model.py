
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy.orm import sessionmaker, Session


from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Time

Base = declarative_base()

# tabelki z pobi

class Klient(Base):
    version_id = Column(Integer, nullable=False)
    __tablename__ = 'klient'
    id = Column(Integer, primary_key=True)
    imie_nazwisko = Column(String)
    wiek = Column(Integer)

class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    tytul = Column(String)
    gatunek = Column(String)
    czas_trwania = Column(Integer)
    data_seansu = Column(String)
    godzina_seansu = Column(Time)
    cena = Column(Float)

class Sala(Base):
    __tablename__ = 'sala'
    id = Column(Integer, primary_key=True)
    numer = Column(Integer)
    nazwa = Column(String)
    pojemnosc = Column(Integer)

class Siedzenie(Base):
    __tablename__ = 'siedzenie'
    id = Column(Integer, primary_key=True)
    rzad = Column(Integer)
    miejsce = Column(Integer)
    sala_id = Column(Integer, ForeignKey('sala.id'))
    sala = relationship("Sala", back_populates="siedzenia")

Sala.siedzenia = relationship("Siedzenie", order_by=Siedzenie.id, back_populates="sala")

class Jedzenie(Base):
    __tablename__ = 'jedzenie'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    typ = Column(String)
    rozmiar = Column(String)
    cena = Column(Float)

class Bilet(Base):
    __tablename__ = 'bilet'
    id = Column(Integer, primary_key=True)
    klient_id = Column(Integer, ForeignKey('klient.id'))
    siedzenie_id = Column(Integer, ForeignKey('siedzenie.id'))
    film_id = Column(Integer, ForeignKey('film.id'))
    klient = relationship("Klient", back_populates="bilety")
    siedzenie = relationship("Siedzenie")
    film = relationship("Film")

Klient.bilety = relationship("Bilet", order_by=Bilet.id, back_populates="klient")

# dziedziczenie

class BiletNormalny(Bilet):
    __tablename__ = 'bilet_normalny'
    id = Column(Integer, ForeignKey('bilet.id'), primary_key=True)
    cena_dodatkowa = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity':'bilet_normalny',
    }

class BiletUlgowy(Bilet):
    __tablename__ = 'bilet_ulgowy'
    id = Column(Integer, ForeignKey('bilet.id'), primary_key=True)
    procent_ulg = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity':'bilet_ulgowy',
    }

# tworzenie bazy sqlite

# tworzenie bazy z poziomem izolacji read committed
engine = create_engine("postgresql://yourusername:yourpassword@localhost:5433/yourdatabase", isolation_level="READ_COMMITTED")


# Create all the tables in the database
Base.metadata.create_all(engine)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()



# regula ACID
try:
    new_klient = Klient(imie_nazwisko="John Doe", wiek=30)
    session.add(new_klient)
    session.commit()
except IntegrityError:
    session.rollback()



# Blokada optymistyczna
klient_to_update = session.query(Klient).filter_by(id=1).first()
if klient_to_update:
    klient_to_update.wiek += 1
    try:
        session.commit()
    except StaleDataError:
        session.rollback()

session = Session()

Base.metadata.create_all(engine)
