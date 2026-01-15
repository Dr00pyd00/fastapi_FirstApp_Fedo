from app.core.database import engine


# Test to know if connexion work with DB
# Check if credentials in SQL_URL are ok.

try:
    connexon = engine.connect()
    print("DB connexion SUCCESS!")
    connexon.close()
except Exception as e:
    print("DB connexion FAILED!")