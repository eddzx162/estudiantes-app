const API = "https://estudiantes-api-gj4f.onrender.com";

let emailGlobal = "";
let estudianteEditando = null;

// 🔐 Enviar OTP
async function sendOTP() {
  const email = document.getElementById("email").value;

  if (!email || !email.includes("@")) {
    alert("Ingresa un correo válido");
    return;
  }

  emailGlobal = email;

  alert("Enviando OTP...");

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

  if (!otp || otp.length < 4) {
    alert("OTP inválido");
    return;
  }

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
        ${e.nombre} - ${e.edad} años - Nota: ${e.nota}
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
  const edad = parseInt(document.getElementById("edad").value);
  const nota = parseFloat(document.getElementById("nota").value);

  if (!nombre) {
    alert("El nombre es obligatorio");
    return;
  }

  if (isNaN(edad) || edad <= 0) {
    alert("Edad inválida");
    return;
  }

  if (isNaN(nota) || nota < 0 || nota > 5) {
    alert("La nota debe estar entre 0 y 5");
    return;
  }

  try {
    await fetch(`${API}/students?nombre=${nombre}&edad=${edad}&nota=${nota}`, {
      method: "POST"
    });

    document.getElementById("nombre").value = "";
    document.getElementById("edad").value = "";
    document.getElementById("nota").value = "";

    cargarEstudiantes();
  } catch (error) {
    console.error(error);
    alert("Error creando estudiante");
  }
}

// ✏️ Abrir modal
function editar(id, nombre, edad, nota) {
  estudianteEditando = id;

  document.getElementById("editNombre").value = nombre;
  document.getElementById("editEdad").value = edad;
  document.getElementById("editNota").value = nota;

  document.getElementById("modal").style.display = "flex";
}

// ❌ Cerrar modal
function cerrarModal() {
  document.getElementById("modal").style.display = "none";
}

// 💾 Guardar cambios
async function guardarEdicion() {
  const nombre = document.getElementById("editNombre").value;
  const edad = parseInt(document.getElementById("editEdad").value);
  const nota = parseFloat(document.getElementById("editNota").value);

  if (!nombre) {
    alert("Nombre obligatorio");
    return;
  }

  if (isNaN(edad) || edad <= 0) {
    alert("Edad inválida");
    return;
  }

  if (isNaN(nota) || nota < 0 || nota > 5) {
    alert("Nota inválida (0 - 5)");
    return;
  }

  try {
    await fetch(`${API}/students/${estudianteEditando}?nombre=${nombre}&edad=${edad}&nota=${nota}`, {
      method: "PUT"
    });

    cerrarModal();
    cargarEstudiantes();
  } catch (error) {
    console.error(error);
    alert("Error actualizando estudiante");
  }
}

// 🗑️ Eliminar
async function eliminar(id) {
  if (!confirm("¿Seguro que quieres eliminar este estudiante?")) return;

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