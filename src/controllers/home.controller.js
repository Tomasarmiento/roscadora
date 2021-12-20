import views from "../views/home.html";
import monitorComponent from "../components/monitor/monitor.component.html";
import { Monitorear } from "../components/monitor/monitor.component";
/*import { MonitorearEstados } from "../controllers/monitorEstados.controller";*/
//import { env } from "../statics/utils/enviroments";


export function MonitorearEstados(dataWs) {
  const indEstadosV = document.getElementsByClassName("estadoV");
  const indEstadosH = document.getElementsByClassName("estadoH");

  for (let i = 0; i < indEstadosV.length; i++) {
    indEstadosV[i].className = "estadoV led led-grey";
  }
  indEstadosV[dataWs.states.vertical.estado].className =
    "estadoV led led-green";

  for (let i = 0; i < indEstadosH.length; i++) {
    indEstadosH[i].className = "estadoH led led-grey";
  }
  indEstadosH[dataWs.states.horizontal.estado].className =
    "estadoH led led-green";
  
}

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

  const selectorCupla = divElement.querySelector("#selectorCupla");

  async function leerTipoCupla() {
    const response = await fetch(`${env.URL_BASE}menu/parametros/`);
    const data = await response.json();
    const indicadorModeloCupla = document.getElementsByClassName("indLargo");       //preguntar a que esta relacionado el modelo de cupla si varian las circuferencias el largo etc
    switch (data.modeloCupla) {
      case 1:
        indicadorModeloCupla[0].className =
          "badge lg-badge badge-pill badge-danger indLargo";
        indicadorModeloCupla[1].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        indicadorModeloCupla[2].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        break;

      case 2:
        indicadorModeloCupla[0].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        indicadorModeloCupla[1].className =
          "badge lg-badge badge-pill badge-danger indLargo";
        indicadorModeloCupla[2].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        break;

      case 3:
        indicadorModeloCupla[0].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        indicadorModeloCupla[1].className =
          "badge lg-badge badge-pill badge-secondary indLargo";
        indicadorModeloCupla[2].className =
          "badge lg-badge badge-pill badge-danger indLargo";
        break;
    }
  }


  selectorCupla.addEventListener("click", (e) => {
    let modeloCupla;
    switch (e.target.id) {
      case "selCuple1":
        document.getElementById(e.target.id).className =
          "badge lg-badge badge-pill badge-danger";
        selCuple2.className = "badge lg-badge badge-pill badge-secondary";
        selCuple3.className = "badge lg-badge badge-pill badge-secondary";
        modeloCupla = 1;
        break;

      case "selCuple2":
        document.getElementById(e.target.id).className =
          "badge lg-badge badge-pill badge-danger";
        selCuple1.className = "badge lg-badge badge-pill badge-secondary";
        selCuple3.className = "badge lg-badge badge-pill badge-secondary";
        modeloCupla = 2;
        break;

      case "selCuple3":
        document.getElementById(e.target.id).className =
          "badge lg-badge badge-pill badge-danger";
        selCuple1.className = "badge lg-badge badge-pill badge-secondary";
        selCuple2.className = "badge lg-badge badge-pill badge-secondary";
        modeloCupla = 3;
        break;
    }

    fetch(`${env.URL_BASE}menu/parametros/`, {
      method: "post",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ modeloCupla: modeloCupla }),
    });
  });

  function envioComando(comando) {
    fetch(`${env.URL_BASE}menu/general/`, {
      method: "post",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ comando: comando }),
    });
  }

  const controlPrincipal = divElement.querySelector("#controlPrincipal");
  controlPrincipal.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "conectar":
        envioComando("conectar");
        break;

      case "modoSafe":
        envioComando("safe");
        break;

      case "reiniciar":
        envioComando("reiniciar");
        break;
    }
  });

  leerTipoCupla();

  Monitorear();

  return divElement;
};