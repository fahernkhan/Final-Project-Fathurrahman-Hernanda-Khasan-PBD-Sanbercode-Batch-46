from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

# Definisikan model dan handler untuk data peminjaman
class Peminjaman(BaseModel):
    aksi: str
    peminjamanid: int = None
    data: dict

@router.post("/api/peminjaman")
def manage_peminjaman(peminjaman: Peminjaman, token: str = Depends(security)):
    # Periksa apakah pengguna memiliki hak admin
    # Lakukan verifikasi JWT token untuk memastikan pengguna adalah admin

    # Kode verifikasi JWT token dan periksa apakah pengguna adalah admin
    # Jika pengguna bukan admin, lempar HTTPException dengan status_code 403 (Forbidden)
    
    # Contoh implementasi sederhana, silakan sesuaikan dengan kebutuhan Anda
    if token != "admin_token":
        raise HTTPException(status_code=403, detail="Access denied. Only admin can access this endpoint.")

    # Jika aksi adalah "N" (tambah peminjaman)
    if peminjaman.aksi == "N":
        # Set tanggal saat ini
        peminjaman.data["tanggal"] = datetime.now().strftime("%Y-%m-%d")

        # Kode untuk menambahkan peminjaman ke basis data
        # return response_sukses
        return {"message": "Peminjaman added successfully"}

    # Jika aksi adalah "E" (ubah peminjaman)
    elif peminjaman.aksi == "E":
        # Kode untuk mengubah data peminjaman di basis data berdasarkan peminjaman.peminjamanid
        # return response_sukses
        return {"message": "Peminjaman updated successfully"}

    else:
        raise HTTPException(status_code=400, detail="Invalid action")