from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def post_user():
    # Kode untuk menambahkan, mengubah, atau menghapus data pengguna
    return {"message": "Post user"}