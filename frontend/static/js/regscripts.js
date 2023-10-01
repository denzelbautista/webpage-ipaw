// Agregar un evento de DOMContentLoaded al objeto document
document.addEventListener("DOMContentLoaded", function () {
  // Obtener el elemento form por su id
  var form = document.getElementById("regForm");

  // Obtener el botón de enviar por su id
  var btn = document.getElementById("btnSend");

  // Agregar un evento de click al botón
  btn.addEventListener("click", function (e) {
    // Prevenir el comportamiento por defecto del botón (enviar el formulario)
    e.preventDefault();

    // Crear un objeto JSON con los datos del formulario
    let data = {
      nombre: document.getElementById("nombre").value,
      apellido: document.getElementById("apellido").value,
      contrasenia: document.getElementById("contrasenia").value,
      dni: document.getElementById("dni").value,
      direccion: document.getElementById("direccion").value,
    };

    // Mostrar el objeto JSON en la consola (opcional)
    console.log(data);

    // Enviar los datos a tu API utilizando fetch
    fetch("http://127.0.0.1:5001/usuarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(() => {
        // Limpiar el formulario
        form.reset();

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
