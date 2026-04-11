import { busquedaDocumentos } from "./api.js";



console.log("JS cargado correctamente");

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM listo");

  const form = document.getElementById("searchForm");

  if (!form) {
    console.error("No se encontró el formulario");
    return;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const query = document.getElementById("searchInput").value;

    if (!query) return;

    try {
      const resultados = await busquedaDocumentos(query);

      console.log("Resultados:", resultados);

      // Guardar búsqueda para usarla en resultados.html
      localStorage.setItem("query", query);

      // Redirigir
      window.location.href = "resultados.html";
    } catch (error) {
      console.error("Error en la búsqueda:", error);
    }
  });
});