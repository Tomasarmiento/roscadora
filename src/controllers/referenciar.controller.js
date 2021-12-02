
import views from "../views/referenciar.html";
import monitorComponent from "../components/monitor/monitor.component.html";



export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

  



  return divElement;
};
