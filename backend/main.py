from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random
import requests
import os

app = FastAPI()

# CORS
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

def enviar_email(destinatario, otp):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": "Bearer re_BJkDBrQA_2jhJ8EqyZDMyUsmarB1PLfvz",
        "Content-Type": "application/json"
    }

    data = {
        "from": "onboarding@resend.dev",
        "to": [destinatario],
        "subject": "Código OTP",
        "html": f"<h2>Tu código OTP es: {otp}</h2>"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print("RESPUESTA EMAIL:", response.text, flush=True)
    except Exception as e:
        print("Error enviando correo:", e, flush=True)


@app.post("/auth/send-otp")
def send_otp(email: str):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    enviar_email(email, otp)

    return {"message": "OTP enviado al correo"}


@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str):
    if otp_storage.get(email) == otp:
        return {"message": "Autenticación exitosa"}
    return {"message": "OTP incorrecto"}

# ------------------ CRUD ------------------

@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM estudiantes")
    rows = cursor.fetchall()
    return [
        {"id": r[0], "nombre": r[1], "edad": r[2], "nota": r[3]}
        for r in rows
    ]

@app.post("/students")
def create_student(nombre: str, edad: int, nota: float):
    cursor.execute(
        "INSERT INTO estudiantes (nombre, edad, nota) VALUES (?, ?, ?)",
        (nombre, edad, nota)
    )
    conn.commit()
    return {"message": "Estudiante creado"}

@app.put("/students/{id}")
def update_student(id: int, nombre: str, edad: int, nota: float):
    cursor.execute(
        "UPDATE estudiantes SET nombre=?, edad=?, nota=? WHERE id=?",
        (nombre, edad, nota, id)
    )
    conn.commit()
    return {"message": "Estudiante actualizado"}

@app.delete("/students/{id}")
def delete_student(id: int):
    cursor.execute("DELETE FROM estudiantes WHERE id=?", (id,))
    conn.commit()
    return {"message": "Estudiante eliminado"}

# ------------------ TEST ------------------

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
