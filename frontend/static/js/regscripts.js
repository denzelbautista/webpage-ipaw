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

    // Enviar el objeto JSON a la ruta del backend con fetch
    fetch("http://127.0.0.1:5001/usuarios", {
      method: "POST", // Especificar el método
      headers: {
        "Content-Type": "application/json", // Especificar el tipo de contenido
      },
      body: JSON.stringify(formJSON, replacer), // Convertir el objeto JSON a una cadena usando la función replacer y usarla como el cuerpo de la solicitud
    })
      .then((response) => response.text()) // Obtener la respuesta como texto
      .then((data) => {
        console.log(data); // Mostrar los datos en la consola (opcional)
        window.location.href = "/"; // Redirigir al index.html
      })
      .catch((error) => console.error(error)); // Manejar los posibles errores
  });
});
