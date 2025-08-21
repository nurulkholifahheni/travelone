from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal

router = APIRouter(prefix="/user-roles", tags=["UserRoles"])  # definisi router untuk tabel pivot user_roles

def get_db():
    db = SessionLocal()  # buat session
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserRole)  # endpoint POST /user-roles
def assign_role(user_role: schemas.UserRole, db: Session = Depends(get_db)):
    # validasi user harus ada
    user = db.query(models.User).filter(models.User.id == user_role.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # validasi role harus ada
    role = db.query(models.Role).filter(models.Role.id == user_role.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # validasi agar tidak assign role yang sama dua kali
    exists = db.query(models.UserRole).filter(
        models.UserRole.user_id == user_role.user_id,
        models.UserRole.role_id == user_role.role_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Role already assigned to user")

    # buat relasi user-role baru
    db_user_role = models.UserRole(user_id=user_role.user_id, role_id=user_role.role_id)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role
