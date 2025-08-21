from fastapi import APIRouter, Depends, HTTPException  # HTTPException untuk validasi error
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal

router = APIRouter(prefix="/roles", tags=["Roles"])  # definisi router untuk role

def get_db():
    db = SessionLocal()  # buat session
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Role)  # endpoint POST /roles
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    # validasi nama role unik
    existing_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing_role:  # jika sudah ada role dengan nama sama
        raise HTTPException(status_code=400, detail="Role already exists")

    # buat role baru
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/", response_model=list[schemas.Role])  # endpoint GET /roles
def read_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()  # ambil semua role
