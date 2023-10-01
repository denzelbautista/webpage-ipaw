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

// para las mascotas

const mascotasPerdidas = [];
let indiceMascotaActual = 0;

function mostrarMascota() {
  const mascotaActual = mascotasPerdidas[indiceMascotaActual];
  document.getElementById("imagen-mascota").src = mascotaActual.image;
  document.getElementById("nombre").textContent = mascotaActual.nombre;
  document.getElementById("descripcion").textContent =
    mascotaActual.descripcion;
  document.getElementById("usuario").textContent = mascotaActual.dni_usuario;
}

function avanzarMascota() {
  indiceMascotaActual++;
  if (indiceMascotaActual >= mascotasPerdidas.length) {
    indiceMascotaActual = 0; // Vuelve al principio si llegamos al final
  }
  mostrarMascota();
}

fetch("http://127.0.0.1:5003/mascotas_perdidas")
  .then((respuesta) => respuesta.json()) // Convertimos el JSON en un objeto
  .then((datos) => {
    // Asignamos el objeto al arreglo de mascotasPerdidas
    mascotasPerdidas = datos;

    // Mostramos la primera mascota
    mostrarMascota();

    // Añadimos el evento click al botón "siguiente"
    document
      .getElementById("siguiente")
      .addEventListener("click", avanzarMascota);
  })
  .catch((error) => {
    // Manejamos el error
    console.error(error);
  });
