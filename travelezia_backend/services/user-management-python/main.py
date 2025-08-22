from fastapi import FastAPI  # import FastAPI class untuk membuat aplikasi
from database import Base, engine  # import Base (metadata) dan engine dari database.py
import models  # import models supaya metadata (tabel) terdaftar di Base
import users, roles, users_roles  # import modul router agar router tersedia untuk di-include

# Buat semua tabel yang didefinisikan di models jika belum ada di database
Base.metadata.create_all(bind=engine)  # memanggil create_all mengaplikasikan skema ke DB

# Inisialisasi instance FastAPI
app = FastAPI(title="User Management Service (Tanpa JWT)")  # buat app dengan judul

# Daftarkan router agar endpoint aktif
app.include_router(users.router)  # register routes dari users.py
app.include_router(roles.router)  # register routes dari roles.py
app.include_router(users_roles.router)  # register routes dari users_roles.py
