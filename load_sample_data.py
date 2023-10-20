
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from combined_kino_db_model import Base, Klient, Film, Sala, Siedzenie, Jedzenie, Bilet, BiletNormalny, BiletUlgowy
import sample_data

def load_sample_data_to_db(session):
    # Insert Klient data
    for klient_data in sample_data.klienci_sample_data:
        new_klient = Klient(imie_nazwisko=klient_data['imie_nazwisko'], wiek=klient_data['wiek'])
        session.add(new_klient)

    # Insert Film data
    for film_data in sample_data.filmy_sample_data:
        new_film = Film(tytul=film_data['tytul'], gatunek=film_data['gatunek'], czas_trwania=film_data['czas_trwania'])
        session.add(new_film)

    # Insert Sala data
    for sala_data in sample_data.sale_sample_data:
        new_sala = Sala(numer=sala_data['numer'], nazwa=sala_data['nazwa'], pojemnosc=sala_data['pojemnosc'])
        session.add(new_sala)

    # Insert Siedzenie data
    for siedzenie_data in sample_data.siedzenia_sample_data:
        new_siedzenie = Siedzenie(rzad=siedzenie_data['rzad'], miejsce=siedzenie_data['miejsce'], sala_id=siedzenie_data['sala_id'])
        session.add(new_siedzenie)

    # Insert Jedzenie data
    for jedzenie_data in sample_data.jedzenie_sample_data:
        new_jedzenie = Jedzenie(typ=jedzenie_data['typ'], rozmiar=jedzenie_data['rozmiar'], cena=jedzenie_data['cena'])
        session.add(new_jedzenie)

    # Insert Bilet data
    for bilet_data in sample_data.bilety_sample_data:
        new_bilet = Bilet(klient_id=bilet_data['klient_id'], siedzenie_id=bilet_data['siedzenie_id'], film_id=bilet_data['film_id'])
        session.add(new_bilet)

    session.commit()

if __name__ == '__main__':
    engine = create_engine('postgresql://username:password@localhost:5433/mydatabase')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    load_sample_data_to_db(session)
