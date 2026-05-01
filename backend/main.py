from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from database import SessionLocal, engine, Base
import models
from email_utils import send_email

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (IMPORTANTE)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# 🔐 AUTH OTP
# -----------------------

@app.post("/auth/send-otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    otp = str(random.randint(100000, 999999))

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        user = models.User(email=email, otp=otp)
        db.add(user)
    else:
        user.otp = otp

    db.commit()

    send_email(email, otp)

    return {"message": "OTP enviado"}

@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or user.otp != otp:
        raise HTTPException(status_code=400, detail="OTP incorrecto")

    return {"message": "Autenticado correctamente"}

# -----------------------
# 👨‍🎓 CRUD STUDENTS
# -----------------------

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.post("/students")
def create_student(nombre: str, edad: int, nota: int, db: Session = Depends(get_db)):
    student = models.Student(nombre=nombre, edad=edad, nota=nota)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, nombre: str, edad: int, nota: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    student.nombre = nombre
    student.edad = edad
    student.nota = nota

    db.commit()
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    db.delete(student)
    db.commit()

    return {"message": "Eliminado"}

    @app.get("/ping")
def ping():
    return {"mensaje": "pong"}