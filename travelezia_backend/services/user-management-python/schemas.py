from pydantic import BaseModel, EmailStr          # BaseModel = class dasar schema Pydantic
                                                 # EmailStr = tipe khusus yang otomatis memvalidasi format email
from typing import Optional, List                # Optional = field boleh None / kosong
                                                 # List = tipe data list (misalnya roles: list[Role])
import uuid                                      # modul uuid dipakai untuk tipe UUID pada user_id


# ===================== ROLE SCHEMAS =====================

class RoleBase(BaseModel):                       # schema dasar Role (dipakai untuk inheritance)
    name: str                                    # field wajib: nama role (contoh: "ADMIN", "USER")
    description: Optional[str] = None            # field opsional: deskripsi role (boleh kosong)

class RoleCreate(RoleBase):                      # schema khusus untuk membuat Role baru
    pass                                         # tidak ada tambahan field (cukup turunan dari RoleBase)

class Role(RoleBase):                            # schema untuk response Role (data ke client)
    id: int                                      # field id role (auto increment di DB)
    class Config:
        from_attributes = True                   # Pydantic v2: ganti `orm_mode=True`, 
                                                 # agar bisa langsung baca dari SQLAlchemy ORM object


# ===================== USER SCHEMAS =====================

class UserBase(BaseModel):                       # schema dasar User (field umum)
    username: str                                # field wajib: username
    email: EmailStr                              # field wajib: email dengan validasi format

class UserCreate(UserBase):                      # schema untuk membuat User baru
    password: str                                # field tambahan: password (plain-text), nanti di-hash di server

class User(UserBase):                            # schema untuk response User (ke client)
    id: uuid.UUID                                # field id (UUID, auto generate di DB)
    is_active: bool                              # status aktif/tidak aktif
    roles: List[Role] = []                       # daftar role yang dimiliki user, default = []
    class Config:
        from_attributes = True                   # konversi otomatis dari SQLAlchemy → JSON response


# ===================== USER UPDATE SCHEMA =====================

class UserUpdate(BaseModel):                     # schema untuk update user
    username: Optional[str] = None               # opsional: jika diisi, update username
    email: Optional[EmailStr] = None             # opsional: jika diisi, update email (tetap divalidasi format email)
    password: Optional[str] = None               # opsional: jika diisi, update password (akan di-hash di server)
    is_active: Optional[bool] = None             # opsional: jika diisi, update status aktif
    class Config:
        from_attributes = True                   # agar schema bisa baca langsung ORM object


# ===================== USER-ROLE SCHEMA =====================

class UserRole(BaseModel):                       # schema untuk pivot table user_roles
    user_id: uuid.UUID                           # field wajib: id user (UUID, FK ke tabel users)
    role_id: int                                 # field wajib: id role (int, FK ke tabel roles)
    class Config:
        from_attributes = True                   # agar schema bisa konversi langsung dari ORM object
