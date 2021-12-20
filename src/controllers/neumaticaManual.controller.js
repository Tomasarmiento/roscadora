import views from "../views/neumaticaManual.html";
import monitorComponent from "../components/monitor/monitor.component.html";
import { ComandosNeumatica } from "../statics/utils/manualNeumatica";
import { Monitorear } from "../components/monitor/monitor.component";

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const monitor = divElement.querySelector("#component-monitor");
  monitor.innerHTML = monitorComponent;

  /*const tituloPagina = document.getElementById("tituloPagina");
  tituloPagina.innerHTML = "MODO MANUAL - Neumatica";
  tituloPagina.className = "h4";*/

  const btns = divElement.querySelector("#contenedorNeumatica");
  const inds = divElement.getElementsByClassName("led");

  btns.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "horizontalCargaOnOff":
        if (inds.horizontalCargaOk.className === "led led-grey") {
          ComandosNeumatica("horizontal", "on");
          inds.horizontalCargaOk.className = "led led-green";
        } else if (inds.horizontalCargaOk.className === "led led-green") {
          ComandosNeumatica("horizontal", "off");
          inds.horizontalCargaOk.className = "led led-grey";
        }
        break;
      case "pinzaCargaOnOff":
        if (inds.pinzaCargaOk.className === "led led-grey") {
          ComandosNeumatica("pinza", "on");
          inds.pinzaCargaOk.className = "led led-green";
        } else if (inds.pinzaCargaOk.className === "led led-green") {
          ComandosNeumatica("pinza", "off");
          inds.pinzaCargaOk.className = "led led-grey";
        }
        break;
      case "verticalCargaOnOff":
        if (inds.verticalCargaOk.className === "led led-grey") {
          ComandosNeumatica("vertical", "on");
          inds.verticalCargaOk.className = "led led-green";
        } else if (inds.verticalCargaOk.className === "led led-green") {
          ComandosNeumatica("vertical", "off");
          inds.verticalCargaOk.className = "led led-grey";
        }
        break;
      case "giroCargaOnOff":
        if (inds.giroCargaOk.className === "led led-grey") {
          ComandosNeumatica("giro", "on");
          inds.giroCargaOk.className = "led led-green";
        } else if (inds.giroCargaOk.className === "led led-green") {
          ComandosNeumatica("giro", "off");
          inds.giroCargaOk.className = "led led-grey";
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
        case "horizontalDescOnOff":
        if (inds.horizontalDescOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.horizontalDescOk.className = "led led-green";
        } else if (inds.horizontalDescOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.horizontalDescOk.className = "led led-grey";
        }
        break;
        case "pinzaDescOnOff":
        if (inds.pinzaDescOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.pinzaDescOk.className = "led led-green";
        } else if (inds.pinzaDescOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.pinzaDescOk.className = "led led-grey";
        }
        break;
        case "verticalBrOnOff":
        if (inds.verticalBrOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.verticalBrOk.className = "led led-green";
        } else if (inds.verticalBrOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.verticalBrOk.className = "led led-grey";
        }
        break;
        case "giroDescOnOff":
        if (inds.giroDescOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.giroDescOk.className = "led led-green";
        } else if (inds.giroDescOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.giroDescOk.className = "led led-grey";
        }
        break;
        case "horizontalBrOnOff":
        if (inds.horizontalBrOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.horizontalBrOk.className = "led led-green";
        } else if (inds.horizontalBrOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.horizontalBrOk.className = "led led-grey";
        }
        break;
        case "pinzaBrOnOff":
        if (inds.pinzaBrOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.pinzaBrOk.className = "led led-green";
        } else if (inds.pinzaBrOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.pinzaBrOk.className = "led led-grey";
        }
        break;
        case "clampeoOnOff":
        if (inds.clampeoOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.clampeoOk.className = "led led-green";
        } else if (inds.clampeoOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.clampeoOk.className = "led led-grey";
        }
        break;
        case "boquilla1OnOff":
        if (inds.boquilla1Ok.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.boquilla1Ok.className = "led led-green";
        } else if (inds.boquilla1Ok.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.boquilla1Ok.className = "led led-grey";
        }
        break;
        case "boquilla2OnOff":
        if (inds.boquilla2Ok.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.boquilla2Ok.className = "led led-green";
        } else if (inds.boquilla2Ok.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.boquilla2Ok.className = "led led-grey";
        }
        break;
        case "boquilla3OnOff":
        if (inds.boquilla3Ok.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.boquilla3Ok.className = "led led-green";
        } else if (inds.boquilla3Ok.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.boquilla3Ok.className = "led led-grey";
        }
        break;
        case "acoplaSolOnOff":
        if (inds.acoplaSolOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.acoplaSolOk.className = "led led-green";
        } else if (inds.acoplaSolOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.acoplaSolOk.className = "led led-grey";
        }
        break;
        case "bombaSolOnOff":
        if (inds.bombaSolOk.className === "led led-grey") {
          ComandosNeumatica("liberar", "on");
          inds.bombaSolOk.className = "led led-green";
        } else if (inds.bombaSolOk.className === "led led-green") {
          ComandosNeumatica("liberar", "off");
          inds.bombaSolOk.className = "led led-grey";
        }
        break;


    }
  });

  Monitorear();
  return divElement;
};
