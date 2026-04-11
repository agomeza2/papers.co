const API_URL = "http://localhost:5000";

// 🔍 Buscar documentos
export async function busquedaDocumentos(query, page = 1) {
  try {
    const respuesta = await fetch(`${API_URL}/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        query,
        page,
        size:10 })
    });

    if (!respuesta.ok) {
      throw new Error("Error en la búsqueda");
    }

    return await respuesta.json();
  } catch (error) {
    console.error("Error en busquedaDocumentos:", error);
    return [];
  }
}

// 📄 Obtener documento por ID
export async function getDocument(id) {
  try {
    const response = await fetch(`${API_URL}/document/${id}`);

    if (!response.ok) {
      throw new Error("Documento no encontrado");
    }

    return await response.json();
  } catch (error) {
    console.error("Error en getDocument:", error);
    return null;
  }
}

// 👤 Obtener autores
export async function getAuthors() {
  try {
    const response = await fetch(`${API_URL}/authors`);
    return await response.json();
  } catch (error) {
    console.error("Error en getAuthors:", error);
    return [];
  }
}

// 🏷️ Obtener keywords
export async function getKeywords() {
  try {
    const response = await fetch(`${API_URL}/keywords`);
    return await response.json();
  } catch (error) {
    console.error("Error en getKeywords:", error);
    return [];
  }
}