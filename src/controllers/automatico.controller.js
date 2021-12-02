import views from "../views/automatico.html";
import monitorComponent from "../components/monitorHorizontal/monitorHorizontal.component.html";
import salidaDeTexto from "../components/cuadroMensajes/cuadroDeTexto.component.html";






export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  
  const monitor = divElement.querySelector("#component-monitor-horizontal");
  monitor.innerHTML = monitorComponent;

  /*const cuadroDeTexto = divElement.querySelector("#salidaDeTexto");
  cuadroDeTexto.innerHTML = salidaDeTexto;*/


  return divElement;
};
