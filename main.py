from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import token
from mysql.connector import connect
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

app = FastAPI()
security = HTTPBearer()
app.include_router(token.router)
class User(BaseModel): 
    aksi: str
    userid: int = None
    data: dict

class Peminjaman(BaseModel): 
    aksi: str
    peminjamanid: int = None
    data: dict

app.include_router(token.router)

def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

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
        database =params.get("MYSQL_DB")
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
    return {"message": "selamat datang di rentalrentalfilm"}

@app.get("/api/movies")
def get_movies():
    # Koneksi ke basis data
    db = connect(
        host=params.get("MYSQL_HOST"),
        user=params.get("MYSQL_USERNAME"),
        password=params.get("MYSQL_PASSWORD"),
        database =params.get("MYSQL_DB"),
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
        database =params.get("MYSQL_DB"),
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

    @app.post("/api/peminjaman")
    def manage_peminjaman(user: User, current_user: dict = Depends(authenticate_user)):
        if current_user["username"] != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

        aksi = peminjaman.aksi
        peminjamanid = peminjaman.peminjamanid
        data = peminjaman.data

        if aksi == "N":
            db = connect(
                host=params.get("MYSQL_HOST"),
                user=params.get("MYSQL_USERNAME"),
                password=params.get("MYSQL_PASSWORD"),
                database =params.get("MYSQL_DB"),
            )
            # Membuat cursor
            cursor = db.cursor(dictionary=True)

            # Query untuk mengambil data peminjaman
            query ="""
                    INSERT INTO peminjaman (movieid, userid, status)
                    VALUES (%(movieid)s, %(userid)s, %(status)s)
                    """

            # Menjalankan query
            cursor.execute(query)

            # Mendapatkan hasil query
            peminjaman = cursor.fetchall()

            # Menutup kursor dan koneksi basis data
            cursor.close()
            db.close()

            # Mengembalikan data peminjaman dalam format JSON
            return peminjaman


        elif aksi == "E":
            db = connect(
                host=params.get("MYSQL_HOST"),
                user=params.get("MYSQL_USERNAME"),
                password=params.get("MYSQL_PASSWORD"),
                database =params.get("MYSQL_DB"),
            )
            # Membuat cursor
            cursor = db.cursor(dictionary=True)

            # Query untuk update data peminjaman
            query = """
                    UPDATE peminjaman
                    SET username = %(username)s, status = %(status)s
                    WHERE id = %(peminjamanid)s
                    """

            # Menjalankan query
            cursor.execute(query)

            # Mendapatkan hasil query
            peminjaman = cursor.fetchall()

            # Menutup kursor dan koneksi basis data
            cursor.close()
            db.close()

            # Mengembalikan data peminjaman dalam format JSON
            return peminjaman
        else:
            raise HTTPException(status_code=400, detail="Invalid action")

        return {"message": message}