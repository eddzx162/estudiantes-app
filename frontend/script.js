const API = "https://estudiantes-api.onrender.com"; // ← pon tu URL real si es distinta

let emailGlobal = "";

// 🔐 Enviar OTP
async function sendOTP() {
  const email = document.getElementById("email").value;
  emailGlobal = email;

  try {
    const res = await fetch(`${API}/auth/send-otp?email=${email}`, {
      method: "POST"
    });

    if (res.ok) {
      document.getElementById("login").style.display = "none";
      document.getElementById("otp").style.display = "block";
    } else {
      alert("Error enviando OTP");
    }
  } catch (error) {
    console.error(error);
    alert("Error de conexión con el servidor");
  }
}

// 🔐 Verificar OTP
async function verifyOTP() {
  const otp = document.getElementById("otpInput").value;

  try {
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
  } catch (error) {
    console.error(error);
    alert("Error de conexión");
  }
}

// 📋 Obtener estudiantes
async function cargarEstudiantes() {
  try {
    const res = await fetch(`${API}/students`);
    const data = await res.json();

    const lista = document.getElementById("lista");
    lista.innerHTML = "";

    data.forEach(e => {
      const li = document.createElement("li");
      li.innerHTML = `
        ${e.nombre} - ${e.edad} - ${e.nota}
        <button onclick="editar(${e.id}, '${e.nombre}', ${e.edad}, ${e.nota})">Editar</button>
        <button onclick="eliminar(${e.id})">Eliminar</button>
      `;
      lista.appendChild(li);
    });

  } catch (error) {
    console.error(error);
    alert("Error cargando estudiantes");
  }
}

// ➕ Crear estudiante
async function crearEstudiante() {
  const nombre = document.getElementById("nombre").value;
  const edad = document.getElementById("edad").value;
  const nota = document.getElementById("nota").value;

  if (!nombre || !edad || !nota) {
    alert("Completa todos los campos");
    return;
  }

  try {
    await fetch(`${API}/students?nombre=${nombre}&edad=${edad}&nota=${nota}`, {
      method: "POST"
    });

    cargarEstudiantes();
  } catch (error) {
    console.error(error);
    alert("Error creando estudiante");
  }
}

// ✏️ Editar estudiante
async function editar(id, nombre, edad, nota) {
  const nuevoNombre = prompt("Nuevo nombre:", nombre);
  const nuevaEdad = prompt("Nueva edad:", edad);
  const nuevaNota = prompt("Nueva nota:", nota);

  if (!nuevoNombre || !nuevaEdad || !nuevaNota) return;

  try {
    await fetch(`${API}/students/${id}?nombre=${nuevoNombre}&edad=${nuevaEdad}&nota=${nuevaNota}`, {
      method: "PUT"
    });

    cargarEstudiantes();
  } catch (error) {
    console.error(error);
    alert("Error actualizando estudiante");
  }
}

// ❌ Eliminar estudiante
async function eliminar(id) {
  try {
    await fetch(`${API}/students/${id}`, {
      method: "DELETE"
    });

    cargarEstudiantes();
  } catch (error) {
    console.error(error);
    alert("Error eliminando estudiante");
  }
}