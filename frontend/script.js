const API = "http://127.0.0.1:8000";

let emailGlobal = "";

// 🔐 Enviar OTP
async function sendOTP() {
  const email = document.getElementById("email").value;
  emailGlobal = email;

  await fetch(`${API}/auth/send-otp?email=${email}`, {
    method: "POST"
  });

  document.getElementById("login").style.display = "none";
  document.getElementById("otp").style.display = "block";
}

// 🔐 Verificar OTP
async function verifyOTP() {
  const otp = document.getElementById("otpInput").value;

  const res = await fetch(`${API}/auth/verify-otp?email=${emailGlobal}&otp=${otp}`, {
    method: "POST"
  });

  if (res.ok) {
    document.getElementById("otp").style.display = "none";
    document.getElementById("app").style.display = "block";
    cargarEstudiantes();
  } else {
    alert("OTP incorrecto");
  }
}

// 📋 Obtener estudiantes
async function cargarEstudiantes() {
  const res = await fetch(`${API}/students`);
  const data = await res.json();

  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  data.forEach(e => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${e.nombre} - ${e.edad} - ${e.nota}
      <button onclick="eliminar(${e.id})">Eliminar</button>
    `;
    lista.appendChild(li);
  });
}

// ➕ Crear estudiante
async function crearEstudiante() {
  const nombre = document.getElementById("nombre").value;
  const edad = document.getElementById("edad").value;
  const nota = document.getElementById("nota").value;

  await fetch(`${API}/students?nombre=${nombre}&edad=${edad}&nota=${nota}`, {
    method: "POST"
  });

  cargarEstudiantes();
}

// ❌ Eliminar estudiante
async function eliminar(id) {
  await fetch(`${API}/students/${id}`, {
    method: "DELETE"
  });

  cargarEstudiantes();
}