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

// scripts-mascotas.js

// Función para obtener y mostrar las mascotas de tipo "perro"
function obtenerMascotas() {
  fetch("http://127.0.0.1:5002/mascotas")
    .then((respuesta) => respuesta.json())
    .then((datos) => {
      if (datos.success && Array.isArray(datos.data)) {
        const mascotasPerro = datos.data.filter(
          (mascota) => mascota.animal === "perro"
        );
        const mascotasContainer = document.getElementById("mascotas-container");

        mascotasPerro.forEach((mascota) => {
          const mascotaDiv = document.createElement("div");
          mascotaDiv.classList.add("mascota-container");

          const imagenMascota = document.createElement("img");
          imagenMascota.src = "/static/images/perro.jpeg"; // Imagen por defecto para perros
          imagenMascota.alt = "Mascota";

          const mascotaDatos = document.createElement("div");
          mascotaDatos.classList.add("mascota-datos");

          const nombre = document.createElement("h3");
          nombre.textContent = mascota.nombre;

          const descripcion = document.createElement("p");
          descripcion.textContent = `Animal: ${mascota.animal}, Raza: ${mascota.raza}`;

          mascotaDatos.appendChild(nombre);
          mascotaDatos.appendChild(descripcion);

          mascotaDiv.appendChild(imagenMascota);
          mascotaDiv.appendChild(mascotaDatos);

          mascotasContainer.appendChild(mascotaDiv);
        });
      } else {
        console.error("Datos no válidos o faltantes en la respuesta.");
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

// Llama a la función para obtener y mostrar las mascotas de tipo "perro" cuando la página cargue
window.addEventListener("load", obtenerMascotas);
