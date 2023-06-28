from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Definisikan model untuk payload
class TokenRequest(BaseModel):
    username: str
    password: str

@router.post("/api/token")
def generate_token(request: TokenRequest):
    # Periksa apakah username dan password valid
    # Jika valid, kirimkan token akses
    # Jika tidak valid, lempar HTTPException dengan status_code 401 (Unauthorized)
    
    # Contoh implementasi sederhana, silakan sesuaikan dengan kebutuhan Anda
    if request.username == "admin" and request.password == "admin123":
        return {"access_token": "your_access_token"}

    # Jika username atau password tidak valid
    raise HTTPException(status_code=401, detail="Invalid username or password")
