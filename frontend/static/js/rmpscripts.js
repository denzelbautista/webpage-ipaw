document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("regMascotasForm");
  const btnEnviar = document.getElementById("btnSendMascotas");

  btnEnviar.addEventListener("click", function () {
    // Obtener los datos del formulario
    const dniUsuario = document.getElementById("dni_usuario").value;
    const nombreMascota = document.getElementById("nombre_mascota").value;
    const animal = document.getElementById("animal").value;
    const raza = document.getElementById("raza").value;
    const image = document.getElementById("image").files[0];
    const descripcion = document.getElementById("descripcion").value;

    // Crear un objeto FormData para enviar datos y archivos
    const formData = new FormData();
    formData.append("dni_usuario", dniUsuario);
    formData.append("nombre", nombreMascota);
    formData.append("animal", animal);
    formData.append("raza", raza);
    formData.append("image", image);
    formData.append("estado", "perdido");
    formData.append("descripcion", descripcion);

    // Enviar los datos a tu API utilizando fetch
    fetch("http://127.0.0.1:5003/mascotas_perdidas", {
      method: "POST",
      body: formData,
    })
      .then(() => {
        // Limpiar el formulario
        formulario.reset();
        // Redirigir al usuario a index.html después de enviar los datos
        // window.location.href = "/";
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
