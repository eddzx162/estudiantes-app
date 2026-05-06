from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText

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


EMAIL_REMITENTE = "eddzxlmgmail.com"
EMAIL_PASSWORD = "fbdq iazz vcjz dhhd"  

def enviar_email(destinatario, otp):
    mensaje = MIMEText(f"Tu código OTP es: {otp}")
    mensaje["Subject"] = "Código OTP"
    mensaje["From"] = EMAIL_REMITENTE
    mensaje["To"] = destinatario

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        servidor.send_message(mensaje)
        servidor.quit()
        print(f"OTP enviado a {destinatario}", flush=True)
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
