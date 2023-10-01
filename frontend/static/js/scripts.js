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

let mascotasPerdidas = [];
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
  .then((respuesta) => respuesta.json())
  .then((datos) => {
    // Verifica que datos.data contenga el arreglo de mascotas
    if (datos.success && datos.data && Array.isArray(datos.data)) {
      // Asigna el arreglo de mascotas a mascotasPerdidas
      mascotasPerdidas = datos.data;

      // Mostramos la primera mascota
      mostrarMascota();

      // Añadimos el evento click al botón "siguiente"
      document
        .getElementById("siguiente")
        .addEventListener("click", avanzarMascota);
    } else {
      console.error("Datos no válidos o faltantes en la respuesta.");
    }
  })
  .catch((error) => {
    console.error(error);
  });
