document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("regMascotasForm");
  const btnEnviar = document.getElementById("btnSendMascotas");

  btnEnviar.addEventListener("click", function () {
    // Obtener los valores de los campos
    let dniUsuario = document.getElementById("dni_usuario").value;
    let nombreMascota = document.getElementById("nombre_mascota").value;
    let animal = document.getElementById("animal").value;
    let raza = document.getElementById("raza").value;

    // Verificar si hay campos vacíos
    if (!dniUsuario || !nombreMascota || !animal || !raza) {
      alert("Por favor, complete todos los campos.");
      return; // Detener el proceso si hay campos vacíos
    }

    // Crear un objeto JSON con los datos del formulario
    let data = {
      dni_usuario: dniUsuario,
      nombre: nombreMascota,
      animal: animal,
      raza: raza,
    };

    // Enviar los datos a tu API utilizando fetch
    fetch("http://127.0.0.1:5002/mascotas", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(() => {
        // Limpiar el formulario
        formulario.reset();
        // Redirigir al usuario a index.html después de enviar los datos
        //window.location.href = "/";
      })
      .catch((error) => {
        console.error("Error al enviar los datos a la API:", error);
      });
  });
});

function redirigirregistro_m_perdidas() {
  window.location.href = "/registro_m_perdidas";
}

function redirigirregistro() {
  window.location.href = "/registro";
}

function redirigirmascota() {
  window.location.href = "/registro_m";
}
function redirigirreserva() {
  window.location.href = "/reserva";
}
function redirigirinicio() {
  window.location.href = "/";
}
