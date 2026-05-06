from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# CORS (para pruebas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIGURACIÓN GMAIL
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "TU_CORREO@gmail.com"
PASSWORD = "TU_APP_PASSWORD"

# Guardar OTP temporal
otp_storage = {}

# Ruta base
@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}

# Enviar OTP
@app.post("/auth/send-otp")
def send_otp(email: str):
    try:
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        mensaje = MIMEText(f"Tu código OTP es: {otp}")
        mensaje["Subject"] = "Código de verificación"
        mensaje["From"] = EMAIL
        mensaje["To"] = email

        print("📧 Intentando enviar OTP a:", email)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, PASSWORD)

        server.sendmail(
            EMAIL,
            email,
            mensaje.as_string()
        )

        server.quit()

        print("✅ OTP enviado:", otp)

        return {"mensaje": "OTP enviado correctamente"}

    except Exception as e:
        print("❌ ERROR SMTP:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Verificar OTP
@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str):
    if email in otp_storage and otp_storage[email] == otp:
        del otp_storage[email]
        return {"mensaje": "OTP verificado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="OTP incorrecto")
