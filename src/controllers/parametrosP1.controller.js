import views from "../views/parametrosP1.html";

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

  function escribirParametros(data) {                                                   //escribe parametros de abajo
    const response = fetch(`${env.URL_BASE}menu/parametros/`, {
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

 
  const formParamsModelo1 = divElement.querySelector(
    "#cuplaModelo1"
  );
  formParamsModelo1.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataModelo1 = Object.fromEntries(
      new FormData(formParamsModelo1)
    );
    escribirParametros(JSON.stringify(dataModelo1));
  });

  const formParamsModelo2= divElement.querySelector(
    "#cuplaModelo2"
  );
  formParamsModelo2.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataModelo2 = Object.fromEntries(
      new FormData(formParamsModelo2)
    );
    escribirParametros(JSON.stringify(dataModelo2));
  });

  const formParamsModelo3 = divElement.querySelector(
    "#cuplaModelo3"
  );
  formParamsModelo3.addEventListener("submit", (e) => {
    e.preventDefault();
    const dataModelo3 = Object.fromEntries(
      new FormData(formParamsModelo3)
    );
    escribirParametros(JSON.stringify(dataModelo3));
  });

  /*const formParamsPalpador = divElement.querySelector("#parametrosPalpador");           //crea una constante1 y llama el id del html 
  formParamsPalpador.addEventListener("submit", (e) => {                                //a la constante1 le dice que este atenta a la interaccion del usuario de tipo submit para ingresar valores
    e.preventDefault();                                                                 //cancela el evento
    const dataPalpador = Object.fromEntries(
      new FormData(formParamsPalpador));                                              //crea una nueva constate2 y lo hace valer la constante1: transforma la lista de pares [clave-valor] en objetos,(compila un conjunto de pares y los envia, transmite los datos tecleados de la primer constante1)
    escribirParametros(JSON.stringify(dataPalpador));                                   //escribe los parametros en menu/parametros/ de tipo post(convierte los datos de la constante2(q son los datos de la constante1 compilados) y los transforma en una cadena de texto JSON)
  });*/

  



  leerParametros(formParamsModelo1);
  leerParametros(formParamsModelo2);                                                    //lee los datos de constante1(funcion leer parametros de arriba)
  leerParametros(formParamsModelo3);

  return divElement;
};
