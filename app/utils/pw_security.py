from passlib.context import CryptContext

pw_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

#======== Func for manage PASSWORDS =============#

def hash_pw(password: str):
    return pw_context.hash(password)

def verify_pw(plain_pw:str, db_pw:str):
    return pw_context.verify(plain_pw, db_pw)