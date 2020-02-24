import csv
from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.schemas import Base, StaticBike
from config import MySQL

if __name__ == "__main__":
    t =time()
    host = MySQL.host
    user = MySQL.username
    password = MySQL.password
    database = MySQL.database

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
    Base.metadata.create_all(engine)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    file_name = "dublin.csv"

    try:
        with open(file_name) as csvfile:
            data = csv.reader(csvfile)
            next(data, None)
            for row in data:
                record = StaticBike(**{
                    'number': row[0],
                    'name': row[1],
                    'address': row[2],
                    'latitude': row[3],
                    'longitude': row[4]
                })
                s.add(record)
            s.commit()

    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection
    print("Time elapsed: " + str(time() - t) + " s.")


