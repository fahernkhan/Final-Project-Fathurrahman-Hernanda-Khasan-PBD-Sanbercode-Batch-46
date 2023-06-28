from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_movies():
    # Kode untuk mengambil data semua film dari basis data
    return {"message": "Get movies"}