import views from "../views/motoresManual.html";
import monitorComponent from "../components/monitor/monitor.component.html";

import { Monitorear } from "../components/monitor/monitor.component";
import { ContinuarDetener } from "../statics/utils/continuarDetener";

function Alert(mensaje) {
  alert(mensaje);
}

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

 
  const btnsHorAxis = divElement.querySelector("#contenedorEjeHorizontal");
  btnsHorAxis.addEventListener("click", (e) => {
    const relPos = divElement.querySelector("#relPos").value;
    const relSpd = divElement.querySelector("#relSpd").value;
    const absPos = divElement.querySelector("#absPos").value;
    const absSpd = divElement.querySelector("#absSpd").value;
    const movExtSpd = divElement.querySelector("#movExtSpd").value;
    switch (e.target.id) {
      case "relFwdH":
        ComandosMotores("adelante", "horizontal", "relativo", relSpd, relPos);
        break;
      case "relBwdH":
        ComandosMotores("atras", "horizontal", "relativo", relSpd, relPos);
        break;
      case "absMoveH":
        ComandosMotores("mover", "horizontal", "absoluto", absSpd, absPos);
        break;
      case "goExtreme1":
        ComandosMotores("ext1", "horizontal", null, movExtSpd, null);
        break;
      case "goExtreme2":
        ComandosMotores("ext2", "horizontal", null, movExtSpd, null);
        break;
      case "horStop":
        ContinuarDetener("detener", null, null, "horizontal");
        break;
    }
  });

  const btnsVerAxis = divElement.querySelector("#contenedorEjeVertical");
  btnsVerAxis.addEventListener("click", (e) => {
    const relPos = divElement.querySelector("#relPosV").value;
    const relSpd = divElement.querySelector("#relSpdV").value;
    const absPos = divElement.querySelector("#absPosV").value;
    const absSpd = divElement.querySelector("#absSpdV").value;
    const movPosSpd = divElement.querySelector("#movPosSpd").value;
    switch (e.target.id) {
      case "upRel":
        ComandosMotores("adelante", "vertical", "relativo", relSpd, relPos);
        break;
      case "downRel":
        ComandosMotores("atras", "vertical", "relativo", relSpd, relPos);
        break;
      case "absMoveV":
        ComandosMotores("mover", "vertical", "absoluto", absSpd, absPos);
        break;
      case "loadPos":
        ComandosMotores("cargac", "vertical", null, movPosSpd, null);
        break;
      case "unloadPos":
        ComandosMotores("liberac", "vertical", null, movPosSpd, null);
        break;
      case "touchProbePress":
        ComandosMotores("presionap", "vertical", null, movPosSpd, null);
        break;
      case "verStop":
        ContinuarDetener("detener", null, null, "vertical");
        break;
    }
  });

  Monitorear();

  return divElement;
};
