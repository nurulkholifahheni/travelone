from sqlalchemy import Column, String, Boolean, Integer, ForeignKey  # import tipe kolom SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID  # import tipe UUID khusus Postgres
from sqlalchemy.orm import relationship  # import helper untuk relasi ORM antar model
import uuid  # import modul untuk generate UUID default
from database import Base  # import Base dari database.py untuk diwarisi model

class User(Base):  # definisi model / tabel 'users'
    __tablename__ = "users"  # nama tabel di database

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # kolom id bertipe UUID, primary key, default random UUID
    username = Column(String(50), unique=True, nullable=False)  # kolom username (unik dan wajib)
    email = Column(String(100), unique=True, nullable=False)  # kolom email (unik dan wajib)
    password_hash = Column(String, nullable=False)  # kolom menyimpan password yang sudah di-hash
    is_active = Column(Boolean, default=True)  # flag apakah akun aktif (default True)

    roles = relationship("UserRole", back_populates="user")  # relasi one-to-many ke UserRole (relasi balik 'user')

class Role(Base):  # definisi model / tabel 'roles'
    __tablename__ = "roles"  # nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # id numeric auto-increment sebagai primary key
    name = Column(String(50), unique=True, nullable=False)  # nama role (contoh: ADMIN, USER), unik dan wajib
    description = Column(String)  # deskripsi opsional

    users = relationship("UserRole", back_populates="role")  # relasi one-to-many ke UserRole (relasi balik 'role')

class UserRole(Base):  # definisi tabel pivot many-to-many antara users dan roles
    __tablename__ = "user_roles"  # nama tabel pivot

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)  # FK ke users.id, bagian PK gabungan
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)  # FK ke roles.id, bagian PK gabungan

    user = relationship("User", back_populates="roles")  # relasi ke model User
    role = relationship("Role", back_populates="users")  # relasi ke model Role
