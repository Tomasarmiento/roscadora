import { pages } from "../controllers/index.controller.js";

let content = document.getElementById("root");

const router = (route) => {
  content.innerHTML = "";
  switch (route) {
    case "#/home":
      return content.appendChild(pages.home());

    case "#/referenciar":
      return content.appendChild(pages.referenciar());
    case "#/automatico":
      return content.appendChild(pages.automatico());
    case "#/neumaticaManual":
      return content.appendChild(pages.neumaticaManual());
    case "#/motoresManual":
      return content.appendChild(pages.motoresManual());
    case "#/sensores":
      return content.appendChild(pages.sensores());
    case "#/monitorEstados":
      return content.appendChild(pages.monitorEstados());
    case "#/semiautomatico":
      return content.appendChild(pages.semiautomatico());
    case "#/parametrosPagina1":
      return content.appendChild(pages.parametrosP1());
    case "#/parametrosPagina2":
      return content.appendChild(pages.parametrosP2());
    default:
      return console.log("404!!!");
  }
};

export { router };