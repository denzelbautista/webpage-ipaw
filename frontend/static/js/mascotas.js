function obtenerMascotas(tipoMascota) {
  // Realiza una solicitud al servidor con el tipo de mascota específico
  fetch(`/mascotas/${tipoMascota}`)
    .then((respuesta) => respuesta.json())
    .then((datos) => {
      if (datos.success && Array.isArray(datos.data)) {
        const categoriaTitulo = document.getElementById("categoriaTitulo");
        categoriaTitulo.textContent = `${
          tipoMascota.charAt(0).toUpperCase() + tipoMascota.slice(1)
        } Registrada :D`;

        const mascotasContainer = document.getElementById("mascotas-container");
        mascotasContainer.innerHTML = ""; // Limpia el contenedor

        datos.data.forEach((mascota) => {
          const mascotaDiv = document.createElement("div");
          mascotaDiv.classList.add("mascota-container");

          const imagenMascota = document.createElement("img");
          imagenMascota.src = `/static/images/${tipoMascota}.jpeg`; // Imagen por defecto según el tipo
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

// Llama a la función para obtener y mostrar las mascotas de un tipo específico cuando la página cargue
window.addEventListener("load", () => {
  // Obtiene el tipo de mascota de la URL y llama a obtenerMascotas con ese tipo
  const path = window.location.pathname;
  const tipoMascota = path.split("/").pop(); // Obtiene la última parte de la URL
  obtenerMascotas(tipoMascota);
});
