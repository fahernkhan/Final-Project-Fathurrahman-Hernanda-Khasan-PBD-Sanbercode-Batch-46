import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Secret key for signing the token
SECRET_KEY = "pbdbatch46"

# Token expiration time (e.g., 1 hour)
TOKEN_EXPIRATION = timedelta(hours=1)

@router.post("/api/token")
def request_token(username: str, password: str):
    if username == "admin" and password == "admin123":
        # Generate the token
        token = generate_token(username)

        # Return the token
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def generate_token(username: str) -> str:
    # Set the token expiration time
    expiration = datetime.utcnow() + TOKEN_EXPIRATION

    # Create the token payload with the username and expiration time
    payload = {"username": username, "exp": expiration}

    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Return the token as a string
    return token.decode("utf-8")
