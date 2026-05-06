from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Permitir todo (para pruebas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "eddzxlm@gmail.com"
PASSWORD = "nigx xlkh wblq qsbg"

# Guardar OTP temporal (memoria)
otp_storage = {}

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/auth/send-otp")
def send_otp(email: str):
    try:
        # Generar código
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        # Crear mensaje
        mensaje = MIMEText(f"Tu código OTP es: {otp}")
        mensaje["Subject"] = "Código de verificación"
        mensaje["From"] = EMAIL
        mensaje["To"] = email

        # Enviar correo
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(mensaje)
        server.quit()

        print("OTP enviado:", otp)

        return {"mensaje": "OTP enviado correctamente"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error enviando correo")


@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str):
    if email in otp_storage and otp_storage[email] == otp:
        del otp_storage[email]
        return {"mensaje": "OTP verificado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="OTP incorrecto")
