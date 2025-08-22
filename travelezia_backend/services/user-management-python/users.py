from fastapi import APIRouter, Depends, HTTPException  # APIRouter untuk router, Depends untuk dependency, HTTPException untuk error handling
from sqlalchemy.orm import Session                       # Session type hint untuk DB session
from passlib.hash import bcrypt                         # bcrypt helper untuk hashing password
from uuid import UUID                                   # UUID type untuk path parameter user_id
import models, schemas                                  # import model dan schema dari project Anda
from database import SessionLocal                       # import session factory dari database.py

router = APIRouter(prefix="/users", tags=["Users"])     # buat router dengan prefix /users dan tag "Users"

def get_db():                                           # dependency function untuk menyediakan DB session ke endpoint
    db = SessionLocal()                                 # buat session baru dari factory
    try:
        yield db                                        # yield session agar bisa dipakai di endpoint (FastAPI akan resume setelah response)
    finally:
        db.close()                                      # pastikan session selalu ditutup ketika request selesai

@router.post("/", response_model=schemas.User)          # endpoint POST /users untuk membuat user baru
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # validasi username unik: cari user dengan username yang sama
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:                                   # jika ditemukan user dengan username sama
        raise HTTPException(status_code=400, detail="Username already registered")  # kembalikan error 400

    # validasi email unik: cari user dengan email yang sama
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:                                  # jika email sudah terdaftar
        raise HTTPException(status_code=400, detail="Email already registered")     # kembalikan error 400

    # validasi panjang password minimal 6 karakter
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")  # kembalikan error jika password pendek

    # hash password sebelum disimpan ke DB (jangan simpan plain password)
    hashed_pw = bcrypt.hash(user.password)

    # buat instance models.User dengan data yang sudah divalidasi dan password yang di-hash
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_pw)
    db.add(db_user)                                      # tambahkan object user ke session
    db.commit()                                          # commit transaksi -> data disimpan ke DB
    db.refresh(db_user)                                  # refresh object agar field yang diisi DB (misal id) tersedia
    return db_user                                       # kembalikan user yang baru dibuat (Pydantic akan serialize sesuai schemas.User)


@router.get("/", response_model=list[schemas.User])     # endpoint GET /users untuk membaca semua user
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()                  # return list semua User dari database


# --------------------------- PUT /users/{user_id} --------------------------------
@router.put("/{user_id}", response_model=schemas.User)  # endpoint PUT untuk update user berdasarkan user_id (UUID)
def update_user(user_id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update user dengan validasi:
    - pastikan user ada (404 jika tidak)
    - jika mengubah username/email, pastikan tidak dipakai user lain (uniqueness)
    - jika mengubah password, lakukan validasi panjang minimal & hash sebelum disimpan
    - jika mengubah is_active, terima perubahan
    """
    # ambil user dari DB berdasarkan user_id (UUID)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:                                      # jika user tidak ditemukan
        raise HTTPException(status_code=404, detail="User not found")  # kembalikan 404

    # ---------------- validate & apply username ----------------
    # hanya jika payload menyertakan username (tidak None) dan berbeda dari yang sekarang
    if user_update.username is not None and user_update.username != db_user.username:
        # cek apakah username baru sudah dipakai user lain (exclude current user lewat id != user_id)
        conflict = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != user_id
        ).first()
        if conflict:                                    # jika ada user lain dengan username yang sama
            raise HTTPException(status_code=400, detail="Username already registered")  # error 400
        # jika lolos cek, assign username baru ke objek DB
        db_user.username = user_update.username

    # ---------------- validate & apply email ----------------
    # hanya jika payload menyertakan email (tidak None) dan berbeda dari yang sekarang
    if user_update.email is not None and str(user_update.email) != str(db_user.email):
        # cek apakah email baru sudah dipakai user lain (exclude current user)
        conflict_email = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != user_id
        ).first()
        if conflict_email:                              # jika ada user lain dengan email sama
            raise HTTPException(status_code=400, detail="Email already registered")  # error 400
        # assign email baru jika lolos validasi
        db_user.email = user_update.email

    # ---------------- validate & apply password ----------------
    # jika payload menyertakan password (ingin diubah)
    if user_update.password is not None:
        # validasi panjang password minimal 6 karakter
        if len(user_update.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")  # error 400
        # hash password baru dan simpan ke kolom password_hash
        db_user.password_hash = bcrypt.hash(user_update.password)

    # ---------------- apply is_active ----------------
    # jika payload menyertakan is_active (bisa True/False)
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active    # update status aktif user

    # setelah semua perubahan diterapkan ke objek db_user, commit ke DB
    db.add(db_user)                                  # tambahkan/update object ke session (opsional, instance sudah ter-attach)
    db.commit()                                      # commit transaksi (simpan perubahan)
    db.refresh(db_user)                              # refresh object agar data terbaru terambil
    return db_user                                   # kembalikan user yang sudah diupdate (diserialisasi oleh pydantic)
