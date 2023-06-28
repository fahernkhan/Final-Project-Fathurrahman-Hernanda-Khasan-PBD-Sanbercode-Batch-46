from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import movies, peminjaman, user, token
from fastapi import Depends
from fastapi import HTTPException
from mysql.connector import connect
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers import peminjaman

app = FastAPI()
security = HTTPBearer()

class User(BaseModel): 
    aksi: str
    userid: int = None
    data: dict

class Peminjaman(BaseModel): 
    aksi: str
    peminjamanid: int = None
    data: dict


def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Kode autentikasi pengguna di sini
    # Anda dapat memeriksa token JWT di credentials.credentials
    # Jika pengguna valid, kembalikan informasi pengguna, misalnya username
    # Jika pengguna tidak valid, raise HTTPException dengan status_code 401

    # Contoh autentikasi sederhana hanya untuk tujuan demonstrasi
    if credentials.credentials == "valid_token":
        return {"username": "admin"}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    
params = dotenv_values(".env")
def execute_query(query, params=None):
    # Koneksi ke basis data
    db = connect(
        host=params.get("MYSQL_HOST"),
        user=params.get("MYSQL_USERNAME"),
        password=params.get("MYSQL_PASSWORD"),
        database="rentalfilm",
    )

    # Membuat cursor
    cursor = db.cursor()

    # Menjalankan query dengan parameter opsional
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    # Commit perubahan
    db.commit()

    # Menutup kursor dan koneksi basis data
    cursor.close()
    db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/api/movies")
def get_movies():
    # Koneksi ke basis data
    db = connect(
        host=params.get("MYSQL_HOST"),
        user=params.get("MYSQL_USERNAME"),
        password=params.get("MYSQL_PASSWORD"),
        database="rentalfilm",
    )

    # Membuat cursor
    cursor = db.cursor(dictionary=True)

    # Query untuk mengambil data semua film
    query = "SELECT * FROM movies"

    # Menjalankan query
    cursor.execute(query)

    # Mendapatkan hasil query
    movies = cursor.fetchall()

    # Menutup kursor dan koneksi basis data
    cursor.close()
    db.close()

    # Mengembalikan data film dalam format JSON
    return JSONResponse(content=movies)

@app.get("/api/peminjaman")
def get_peminjaman(current_user: dict = Depends(authenticate_user)):
    # Koneksi ke basis data
    db = connect(
        host=params.get("MYSQL_HOST"),
        user=params.get("MYSQL_USERNAME"),
        password=params.get("MYSQL_PASSWORD"),
        database="rentalfilm",
    )

    # Membuat cursor
    cursor = db.cursor(dictionary=True)

    # Query untuk mengambil data peminjaman
    if current_user["username"] == "admin":
        # Jika pengguna adalah admin, ambil semua data peminjaman
        query = "SELECT * FROM peminjaman"
    else:
        # Jika pengguna adalah pengguna biasa, ambil data peminjaman pengguna tersebut
        query = "SELECT * FROM peminjaman WHERE userid = %(userid)s"
        cursor.execute(query, {"userid": current_user["userid"]})

    # Menjalankan query
    cursor.execute(query)

    # Mendapatkan hasil query
    peminjaman = cursor.fetchall()

    # Menutup kursor dan koneksi basis data
    cursor.close()
    db.close()

    # Mengembalikan data peminjaman dalam format JSON
    return peminjaman

@app.post("/api/user")
def manage_user(user: User, current_user: dict = Depends(authenticate_user)):
    if current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    # Ekstraksi data dari body request
    aksi = user.aksi
    userid = user.userid
    data = user.data

    if aksi == "N":
        # Menambahkan pengguna baru
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        # Query untuk menambahkan pengguna baru
        query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
        params = (username, password, email)

        execute_query(query, params)
        message = "User added successfully"
    elif aksi == "E":
        # Mengubah data pengguna
        username = data.get("username")

        # Query untuk mengubah data pengguna
        query = "UPDATE user SET username = %s WHERE userid = %s"
        params = (username, userid)

        execute_query(query, params)
        message = "User updated successfully"
    elif aksi == "D":
        # Menghapus pengguna
        # Query untuk menghapus pengguna
        query = "DELETE FROM user WHERE userid = %s"
        params = (userid,)

        execute_query(query, params)
        message = "User deleted successfully"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    return {"message": message}

app.include_router(peminjaman.router)

app.include_router(token.router)


