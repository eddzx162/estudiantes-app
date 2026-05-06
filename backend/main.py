from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 API KEY SENDA SERVICE
SENDA_API_KEY = "TU_API_KEY_AQUI"

# Guardar OTP
otp_storage = {}

# ------------------ ROOT ------------------
@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}

# ------------------ ENVIAR OTP ------------------
@app.post("/auth/send-otp")
def send_otp(email: str):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    try:
        response = requests.post(
            "https://api.senda-service.com/v1/email/send",
            headers={
                "Authorization": f"Bearer {SENDA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "no-reply@senda-service.com",
                "to": email,
                "subject": "Código OTP",
                "html": f"<h2>Tu código OTP es: {otp}</h2>"
            }
        )

        print("Respuesta Senda:", response.text)

        if response.status_code != 200:
            raise Exception(response.text)

        return {"mensaje": "OTP enviado correctamente"}

    except Exception as e:
        print("❌ ERROR SENDA:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ VERIFICAR OTP ------------------
@app.post("/auth/verify-otp")
def verify_otp(email: str, otp: str):
    if email in otp_storage and otp_storage[email] == otp:
        del otp_storage[email]
        return {"mensaje": "OTP verificado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="OTP incorrecto")
