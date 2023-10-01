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
  console.log("Clic en 'Siguiente'");
  indiceMascotaActual++;
  console.log("Índice actual: " + indiceMascotaActual);

  if (indiceMascotaActual >= mascotasPerdidas.length) {
    indiceMascotaActual = 0; // Vuelve al principio si llegamos al final
    console.log("Reiniciando a 0");
  }

  console.log("Nuevo índice: " + indiceMascotaActual);

  mostrarMascota();
}

async function obtenerMascotas() {
  try {
    const respuesta = await fetch("http://127.0.0.1:5003/mascotas_perdidas");
    const datos = await respuesta.json();

    if (datos.success && datos.data && Array.isArray(datos.data)) {
      mascotasPerdidas = datos.data;
      console.log(mascotasPerdidas);
      mostrarMascota();
    } else {
      console.error("Datos no válidos o faltantes en la respuesta.");
    }
  } catch (error) {
    console.error(error);
  }
}

// Llama a obtenerMascotas al cargar la página
obtenerMascotas().then(() => {
  // Añade el evento click al botón "siguiente" después de cargar los datos
  document
    .getElementById("siguiente")
    .addEventListener("click", avanzarMascota);
});
