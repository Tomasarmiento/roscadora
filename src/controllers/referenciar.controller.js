import views from "../views/referenciar.html";
import monitorComponent from "../components/monitor/monitor.component.html";
//import { env } from "../statics/utils/enviroments";         //ENV CON LA IP NO CREADO AÚN
import { Monitorear } from "../components/monitor/monitor.component";

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

  /*const tituloPagina = document.getElementById("tituloPagina");
  tituloPagina.innerHTML = "REFERENCIAR";
  tituloPagina.className = "h3";*/           //TITULO DE PAGINA EN LA QUE ESTOY

  const controles = divElement.querySelector("#homeExec");
  controles.addEventListener("click", async (e) => {
    const response = await fetch(env.URL_BASE + "menu/referenciar/", {
      method: "post",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ comando: "referenciar" }),
    });
  });

  Monitorear();

  return divElement;
};
