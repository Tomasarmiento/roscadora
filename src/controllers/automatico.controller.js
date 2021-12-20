import views from "../views/automatico.html";
import monitorComponent from "../components/monitorHorizontal/monitorHorizontal.component.html";
import graficoRoscado from "../components/grafico/graficoRoscado.component.html";
import { ContinuarDetener } from "../statics/utils/continuarDetener";
//import salidaDeTexto from "../components/cuadroMensajes/cuadroDeTexto.component.html";
//import { Graficar } from "../statics/utils/generarGrafico"; funcion graficar no hecha por falta de datos

export default () => {
  async function leerParametros(form) {
    const response = await fetch(`${env.URL_BASE}menu/parametros/`);
    const data = await response.json();
    const parametros = new Map(Object.entries(data));
    const formKeys = new FormData(form);
    const map = new Map();

    /*for (var key of formKeys.keys()) {
      map.set(key, parametros.get(key));
    }
    const oTabla = Object.fromEntries(map);

    for (var key of Object.keys(oTabla)) {
      const campo = document.getElementsByName(key)[0];
      campo.value = oTabla[key];
    }*/
  }

  function escribirParametros(data) {                                      //manda JSON de recuadro de valores
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

  const monitor = divElement.querySelector("#component-monitor-horizontal");
  monitor.innerHTML = monitorComponent;

  const graficoEnderezado = divElement.querySelector(
    "#component-grafico-roscado"
  );
  graficoEnderezado.innerHTML = graficoRoscado;
  
  /*const cuadroDeTexto = divElement.querySelector("#salidaDeTexto");                               //salida de texto no lo usamos por ahora
  cuadroDeTexto.innerHTML = salidaDeTexto;*/


  /*const tituloPagina = document.getElementById("tituloPagina");
  tituloPagina.innerHTML = "MODO AUTOMATICO - Proceso";
  tituloPagina.className = "h5";*/

  const controles = divElement.querySelector("#contenedor-continuarDetener");
  controles.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "continue":
        ContinuarDetener(
          "continuar",
          window.location.hash.split("#/")[1].split("A")[0],
          "automatico"
        );
        break;
      case "stop":
        ContinuarDetener(
          "detener",
          window.location.hash.split("#/")[1].split("A")[0],
          "automatico"
        );
        break; 
      /*case "refrescar":                                            boton de refrescar para agregar a futuro
        Graficar("line", "Deformacion", 1, "esc", 1);
        break;*/
    }
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

  //Graficar("line", "Deformacion", 1, "esc", 1);        funcion graficar no hecha por falta de datos

  leerParametros(formParamsModelo3);

  return divElement;
};
