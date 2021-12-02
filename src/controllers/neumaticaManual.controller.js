import views from "../views/neumaticaManual.html";
import monitorComponent from "../components/monitor/monitor.component.html";

import { ContinuarDetener } from "../statics/utils/continuarDetener";
import { Monitorear } from "../components/monitor/monitor.component";

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

  

  const btns = divElement.querySelector("#contenedorNeumatica");
  const inds = divElement.getElementsByClassName("led");

  btns.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "horizontalOnOff":
        if (inds.horizontalOk.className === "led led-grey") {
          ComandosNeumatica("horizontal", "on");
          inds.horizontalOk.className = "led led-green";
        } else if (inds.horizontalOk.className === "led led-green") {
          ComandosNeumatica("horizontal", "off");
          inds.horizontalOk.className = "led led-grey";
        }
        break;
      case "pinzaOnOff":
        if (inds.pinzaOk.className === "led led-grey") {
          ComandosNeumatica("pinza", "on");
          inds.pinzaOk.className = "led led-green";
        } else if (inds.pinzaOk.className === "led led-green") {
          ComandosNeumatica("pinza", "off");
          inds.pinzaOk.className = "led led-grey";
        }
        break;
      case "verticalOnOff":
        if (inds.verticalOk.className === "led led-grey") {
          ComandosNeumatica("vertical", "on");
          inds.verticalOk.className = "led led-green";
        } else if (inds.verticalOk.className === "led led-green") {
          ComandosNeumatica("vertical", "off");
          inds.verticalOk.className = "led led-grey";
        }
        break;
      case "giroOnOff":
        if (inds.giroOk.className === "led led-grey") {
          ComandosNeumatica("giro", "on");
          inds.giroOk.className = "led led-green";
        } else if (inds.giroOk.className === "led led-green") {
          ComandosNeumatica("giro", "off");
          inds.giroOk.className = "led led-grey";
        }
        break;
      case "liberarOnOff":
        if (inds.liberarOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.liberarOk.className = "led led-green";
        } else if (inds.liberarOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.liberarOk.className = "led led-grey";
        }
        break;
        
      case "giroCuchilla":
        ComandosNeumatica("secuencia_giro", "giro");
        break;
        
      case "stop":
        ContinuarDetener(
          "detener",
          window.location.hash.split("#/")[1].split("A")[0],
          "automatico"
        );
        break;
    }
  });

  Monitorear();
  return divElement;
};
