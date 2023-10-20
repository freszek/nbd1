
from sqlalchemy.orm import Session
from combined_kino_db_model import Klient, Film, engine  # Import additional tables as needed
from sample_data import sample_data

# Create a new session
session = Session(engine)

# Function to load sample data into the database
def load_sample_data_to_db():
    # Loop through each table name and its data in sample_data
    for table, records in sample_data.items():
        # Dynamically insert data based on table name
        if table == 'Klienci':
            for record in records:
                new_record = Klient(**record)
                session.add(new_record)
        elif table == 'Film':
            for record in records:
                new_record = Film(**record)
                session.add(new_record)
        # Add more elif conditions for additional tables
                
    # Commit the transaction
    session.commit()

# Load the sample data
if __name__ == '__main__':
    load_sample_data_to_db()
