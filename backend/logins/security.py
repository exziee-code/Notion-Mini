from pwdlib import PasswordHash

hash_password = PasswordHash.recommended()

def HashPassword(password: str) -> str:
    return hash_password.hash(password)

def verify_password(typed_password: str, hashed_password: str) -> bool:
    return hash_password.verify(typed_password, hashed_password)