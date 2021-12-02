import views from "../views/home.html";
import monitorComponent from "../components/monitor/monitor.component.html";

export default () => {
  const divElement = document.createElement("div");
  
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

 
  return divElement;
};