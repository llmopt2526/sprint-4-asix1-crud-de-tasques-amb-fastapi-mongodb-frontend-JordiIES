const API = "http://localhost:8000";

// Carrega tots els llibres i els posa a la taula + filtratge
async function loadBooks() {
  const cat   = document.getElementById("filtreCat").value.trim();
  const estat = document.getElementById("filtreEstat").value;

  let url = API + "/llibres/?";
  if (cat)   url += "categoria=" + encodeURIComponent(cat) + "&";
  if (estat) url += "estat=" + estat;

  const res  = await fetch(url);
  const data = await res.json();

  const tbody = document.getElementById("bodyLlibres");
  tbody.innerHTML = "";

  data.llibres.forEach(function(l) {
    tbody.innerHTML += "<tr>" +
      "<td>" + l.titol + "</td>" +
      "<td>" + l.autor + "</td>" +
      "<td><span class='estat-" + l.estat + "'>" + l.estat.charAt(0).toUpperCase() + l.estat.slice(1) + "</span></td>" +
      "<td>" + (l.valoracio ?? "-") + "</td>" +
      "<td>" + l.categoria + "</td>" +
      "<td>" + l.persona + "</td>" +
      "<td>" +
        "<button class='petit' onclick=\"editBook('" + l._id + "')\">Editar</button> " +
        "<button class='petit eliminar' onclick=\"deleteBook('" + l._id + "')\">Eliminar</button>"
      "</td>" +
    "</tr>";
  });
}

// Crea o edta un llibre segons si hi ha ID
async function saveBook() {
  const id = document.getElementById("editId").value;
  const val = document.getElementById("valoracio").value;

  const dades = {
    titol:     document.getElementById("titol").value,
    autor:     document.getElementById("autor").value,
    estat:     document.getElementById("estat").value,
    valoracio: val ? parseInt(val) : null,
    categoria: document.getElementById("categoria").value,
    persona:   document.getElementById("persona").value,
  };

  if (!dades.titol || !dades.autor || !dades.categoria || !dades.persona) {
    alert("Omple tots els camps obligatoris.");
  return;
  }
  
  if (dades.estat === "pendent" && dades.valoracio) {
    alert("No pots puntuar un llibre que encara no has llegit.");
    return;
  }

  await fetch(API + "/llibres/" + (id ? id : ""), {
    method:  id ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(dades),
  });

  resetForm();
  loadBooks();
}

// Omple el formulari per editar
async function editBook(id) {
  const res = await fetch(API + "/llibres/" + id);
  const l   = await res.json();

  document.getElementById("editId").value    = l._id;
  document.getElementById("titol").value     = l.titol;
  document.getElementById("autor").value     = l.autor;
  document.getElementById("estat").value     = l.estat;
  document.getElementById("valoracio").value = l.valoracio ?? "";
  document.getElementById("categoria").value = l.categoria;
  document.getElementById("persona").value   = l.persona;
  document.getElementById("formCard").classList.add("editant");
  document.getElementById("formTitle").textContent = "Editar llibre";
}

// Elmina un llibre
async function deleteBook(id) {
  if (confirm("Eliminar aquest llibre?")) {
    await fetch(API + "/llibres/" + id, { method: "DELETE" });
    loadBooks();
  }
}

// Buida el formulari
function resetForm() {
  ["editId","titol","autor","valoracio","categoria","persona"].forEach(function(id) {
    document.getElementById(id).value = "";
  });
  document.getElementById("estat").value = "pendent";
  document.getElementById("formCard").classList.remove("editant");
  document.getElementById("formTitle").textContent = "Nou llibre";
}

// Netejar filtres
function clearFiltres() {
  document.getElementById("filtreCat").value = "";
  document.getElementById("filtreEstat").value = "";
  loadBooks();
}

// Inicia la pàgina
loadBooks();