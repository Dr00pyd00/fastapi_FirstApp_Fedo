from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# creation url with all data for connexion:
SQL_ALCHEMY_URL = "postgresql://postgres:luna@localhost/FirstAppDB"

# creation engine:
engine = create_engine(url=SQL_ALCHEMY_URL)

# creation voiture: db____app 
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


#=========== BASE FOR TABLES ===========#
    # for regroup all tables in the db.
Base = declarative_base()

#=========== DEPENDS FOR DB ============#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()