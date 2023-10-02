document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("reservaForm");
  var btn = document.getElementById("btnReservar");
  var table = document.querySelector(".reservas-table tbody");

  function cargarReservas() {
    fetch("http://127.0.0.1:5004/reservas")
      .then((response) => response.json())
      .then((data) => {
        table.innerHTML = "";

        if (data.data) {
          data.data.forEach(function (reserva) {
            // Obtener información completa de la mascota usando su ID
            fetch(`http://127.0.0.1:5002/mascotas/${reserva.id_mascota}`)
              .then((response) => response.json())
              .then((mascotaData) => {
                // Verificar si se encontró la mascota
                if (mascotaData.data) {
                  var mascota = mascotaData.data;
                  var row = table.insertRow();
                  row.insertCell(0).textContent = mascota.nombre; // Mostrar el nombre de la mascota
                  row.insertCell(1).textContent = reserva.servicio;
                  row.insertCell(2).textContent = reserva.f_inicio;
                  row.insertCell(3).textContent = reserva.f_fin;
                } else {
                  alert("No se encontró información de la mascota.");
                }
              })
              .catch((error) => {
                console.error(
                  "Error al obtener información de la mascota:",
                  error
                );
              });
          });
        }
      })
      .catch((error) => {
        console.error("Error al obtener las reservas:", error);
      });
  }

  function obtenerIdMascotaPorNombre(nombreMascota, callback) {
    fetch("http://127.0.0.1:5002/mascotas")
      .then((response) => response.json())
      .then((data) => {
        if (data.data) {
          const mascotaEncontrada = data.data.find(
            (mascota) => mascota.nombre === nombreMascota
          );
          if (mascotaEncontrada) {
            callback(mascotaEncontrada.id);
          } else {
            alert("La mascota no existe.");
          }
        }
      })
      .catch((error) => {
        console.error("Error al obtener las mascotas:", error);
      });
  }

  btn.addEventListener("click", function (e) {
    e.preventDefault();
    var formData = new FormData(form);
    var nombreMascota = formData.get("id_mascota");

    obtenerIdMascotaPorNombre(nombreMascota, function (idMascota) {
      // Crear un objeto JSON con los datos del formulario
      var reservaData = {
        dni_usuario: formData.get("dni_usuario"),
        id_mascota: idMascota,
        servicio: formData.get("servicio"),
        f_inicio: formData.get("f_inicio"),
        f_fin: formData.get("f_fin"),
      };

      // Enviar los datos a la API de reservas utilizando fetch
      fetch("http://127.0.0.1:5004/reservas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reservaData),
      })
        .then(() => {
          form.reset();
          cargarReservas();
        })
        .catch((error) => {
          console.error("Error al enviar los datos a la API:", error);
        });
    });
  });

  cargarReservas();
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
