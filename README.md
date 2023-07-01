# Final-Project-Fathurrahman-Hernanda-Khasan-PBD-Sanbercode-Batch-46
project akhir sanbercode

Membuat sebuah Sistem REST API menggunakan framework FastAPI. Sistem ini akan memiliki dua jenis pengguna, yaitu admin dan pengguna biasa. Admin dapat melihat semua data peminjaman dari semua pengguna, sedangkan pengguna biasa hanya dapat melihat peminjaman yang dilakukan oleh pengguna tersebut

GET /api/movies: Digunakan untuk mengambil data semua film.

GET /api/peminjaman: Digunakan untuk mengambil semua data peminjaman. Endpoint ini dilindungi menggunakan JWT. Admin dapat melihat semua peminjaman dari semua pengguna, sedangkan pengguna biasa hanya dapat melihat peminjaman mereka sendiri.

POST /api/user/: Hanya dapat diakses oleh admin dan dilindungi menggunakan JWT. Digunakan untuk menambahkan, mengubah, dan menghapus data pengguna. Anda perlu mengirimkan permintaan dengan payload yang sesuai dengan tindakan yang diinginkan (tambah, ubah, atau hapus) dan data pengguna yang relevan.

POST /api/peminjaman: Digunakan untuk menambahkan dan mengubah data peminjaman. Endpoint ini hanya dapat diakses oleh admin dan dilindungi menggunakan JWT. Anda perlu mengirimkan permintaan dengan payload yang sesuai dengan tindakan yang diinginkan (tambah atau ubah) dan data peminjaman yang relevan. Tanggal akan diinput secara otomatis saat data ditambahkan. Status peminjaman bernilai 1 atau 0, dengan 1 berarti sedang aktif (ada pinjaman) dan 0 berarti non-aktif (film telah dikembalikan).

POST /api/token: Digunakan untuk meminta token akses baru. Anda perlu menggunakan kode rahasia "pbdbatch46" dan mengirimkan username dan password sebagai payload.
