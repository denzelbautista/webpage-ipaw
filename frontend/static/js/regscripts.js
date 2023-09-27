// vamos a hacer que funcione el registro de usuarios
// 1. capturar el evento submit del formulario
// 2. prevenir el comportamiento por defecto
// 3. capturar los datos del formulario
// 4. validar los datos del formulario
// 5. enviar los datos al backend
// 6. recibir la respuesta del backend
// 7. mostrar el mensaje de error o de éxito

// Obtener el elemento form por su id
var form = document.getElementById("regForm");

// Obtener el botón de enviar por su id
var btn = document.getElementById("btnSend");

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

  // Enviar el objeto JSON a la ruta del backend con fetch
  fetch("/usuarios", {
    method: "POST", // Especificar el método POST
    headers: {
      "Content-Type": "application/json", // Especificar el tipo de contenido
    },
    body: JSON.stringify(formJSON), // Convertir el objeto JSON a una cadena y usarla como el cuerpo de la solicitud
  })
    .then((response) => response.text()) // Obtener la respuesta como texto
    .then((data) => console.log(data)) // Mostrar los datos en la consola (opcional)
    .catch((error) => console.error(error)); // Manejar los posibles errores
});
