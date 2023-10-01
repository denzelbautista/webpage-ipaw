// vamos a hacer que funcione el registro de usuarios
// 1. capturar el evento submit del formulario
// 2. prevenir el comportamiento por defecto
// 3. capturar los datos del formulario
// 4. validar los datos del formulario
// 5. enviar los datos al backend
// 6. recibir la respuesta del backend
// 7. mostrar el mensaje de error o de éxito

// Agregar un evento de DOMContentLoaded al objeto document
document.addEventListener("DOMContentLoaded", function () {
  // Obtener el elemento form por su id
  var form = document.getElementById("reservaForm");

  // Obtener el botón de enviar por su id
  var btn = document.getElementById("btnReservar");

  // Agregar un evento de click al botón
  btn.addEventListener("click", function (e) {
    // Prevenir el comportamiento por defecto del botón (enviar el formulario)
    e.preventDefault();

    // Crear un objeto FormData con los datos del formulario
    var formData = new FormData(form);

    // Convertir el objeto FormData a un objeto JSON
    var formJSON = Object.fromEntries(formData.entries());

    // Mostrar el objeto JSON en la consola (opcional)
    console.log(formJSON);

    // Crear una función que reemplace los valores no válidos por null
    function replacer(key, value) {
      if (value === undefined || value === NaN || typeof value === "function") {
        return null;
      }
      return value;
    }

    // Enviar los datos a tu API utilizando fetch
    fetch("URL_de_tu_API", {
      method: "POST",
      body: formData,
    })
      .then(() => {
        // Limpiar el formulario
        formulario.reset();
        // Redirigir al usuario a index.html después de enviar los datos
        window.location.href = "/";
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
