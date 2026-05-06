from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random
import requests
import os

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DATABASE ------------------
conn = sqlite3.connect("estudiantes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad INTEGER,
    nota REAL
)
""")
conn.commit()

# ------------------ OTP ------------------
otp_storage = {}

# API KEY desde variables de entorno (Render)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# Enviar OTP
@app.post("/auth/send-otp")
def send_otp(email: str):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": [email],
                "subject": "Código OTP",
                "html": f"<h2>Tu código OTP es: {otp}</h2>"
            }
        )

        print("RESEND:", response.status_code, response.text)

        if response.status_code not in [200, 201]:
            raise Exception(response.text)

        return {"mensaje": "OTP enviado correctamente"}

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Verificar OTP
@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str):
    if email in otp_storage and otp_storage[email] == otp:
        del otp_storage[email]
        return {"mensaje": "Autenticación exitosa"}
    else:
        raise HTTPException(status_code=400, detail="OTP incorrecto")

# ------------------ CRUD ------------------

# Obtener estudiantes
@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM estudiantes")
    rows = cursor.fetchall()
    return [
        {"id": r[0], "nombre": r[1], "edad": r[2], "nota": r[3]}
        for r in rows
    ]

# Crear estudiante
@app.post("/students")
def create_student(nombre: str, edad: int, nota: float):
    cursor.execute(
        "INSERT INTO estudiantes (nombre, edad, nota) VALUES (?, ?, ?)",
        (nombre, edad, nota)
    )
    conn.commit()
    return {"message": "Estudiante creado"}

# Actualizar estudiante
@app.put("/students/{id}")
def update_student(id: int, nombre: str, edad: int, nota: float):
    cursor.execute(
        "UPDATE estudiantes SET nombre=?, edad=?, nota=? WHERE id=?",
        (nombre, edad, nota, id)
    )
    conn.commit()
    return {"message": "Estudiante actualizado"}

# Eliminar estudiante
@app.delete("/students/{id}")
def delete_student(id: int):
    cursor.execute("DELETE FROM estudiantes WHERE id=?", (id,))
    conn.commit()
    return {"message": "Estudiante eliminado"}

# ------------------ TEST ------------------
@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
