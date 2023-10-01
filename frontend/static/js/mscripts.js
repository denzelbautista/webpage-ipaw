document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("regMascotasForm");
  const btnEnviar = document.getElementById("btnSendMascotas");

  btnEnviar.addEventListener("click", function () {
    // Crear un objeto JSON con los datos del formulario
    let data = {
      dni_usuario: document.getElementById("dni_usuario").value,
      nombre: document.getElementById("nombre_mascota").value,
      animal: document.getElementById("animal").value,
      raza: document.getElementById("raza").value,
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
