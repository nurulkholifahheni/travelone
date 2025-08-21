from sqlalchemy import create_engine  # import fungsi untuk membuat engine koneksi ke DB
from sqlalchemy.ext.declarative import declarative_base  # import base class untuk model SQLAlchemy
from sqlalchemy.orm import sessionmaker  # import pembuat session (factory) untuk koneksi DB

# URL koneksi ke PostgreSQL (username: postgres, password: heninurul, host: localhost, port: 5432, db: travelone)
DATABASE_URL = "postgresql+psycopg2://postgres:heninurul@localhost:5432/travelone"  # string koneksi DB

# Buat engine SQLAlchemy yang mengeksekusi koneksi ke DB berdasarkan DATABASE_URL
engine = create_engine(DATABASE_URL)  # engine digunakan untuk menjalankan query dan membuat metadata binding

# Buat SessionLocal sebagai factory session; setiap panggilan SessionLocal() memberi session baru
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # sessionmaker mengatur transaksi

# Base class yang dipakai sebagai parent untuk semua model (metadata tersimpan di sini)
Base = declarative_base()  # Base.metadata berisi semua table definitions
