import views from "../views/parametrosP2.html";


export default () => {
  async function leerParametros(form) {
    const response = await fetch(`${env.URL_BASE}menu/parametros/`);
    const data = await response.json();
    const parametros = new Map(Object.entries(data));
    const formKeys = new FormData(form);
    const map = new Map();

    for (var key of formKeys.keys()) {
      map.set(key, parametros.get(key));
    }
    const oTabla = Object.fromEntries(map);

    for (var key of Object.keys(oTabla)) {
      const campo = document.getElementsByName(key)[0];
      campo.value = oTabla[key];
    }
  }

  function escribirParametros(data) {
    fetch(`${env.URL_BASE}menu/parametros/`, {
      method: "post",
      headers: {
        "content-type": "application/json",
      },
      body: data,
    });
  }
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;


  const formParamsCuchillas = divElement.querySelector("#parametrosCuchillas");
  formParamsCuchillas.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataCuchillas = Object.fromEntries(new FormData(formParamsCuchillas));
    escribirParametros(JSON.stringify(dataCuchillas));
  });

  const formParamsEjeVertical = divElement.querySelector(
    "#parametrosEjeVertical"
  );
  formParamsEjeVertical.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataEjeVertical = Object.fromEntries(
      new FormData(formParamsEjeVertical)
    );
    escribirParametros(JSON.stringify(dataEjeVertical));
  });

  const formParamsEnderezado = divElement.querySelector(
    "#parametrosEnderezado"
  );
  formParamsEnderezado.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataEnderezado = Object.fromEntries(
      new FormData(formParamsEnderezado)
    );
    escribirParametros(JSON.stringify(dataEnderezado));
  });

  leerParametros(formParamsCuchillas);
  leerParametros(formParamsEjeVertical);
  leerParametros(formParamsEnderezado);

  return divElement;
};
