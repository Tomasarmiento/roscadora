import views from "../views/semiautomatico.html";
import { SemiAutomatico } from "../statics/utils/semiAutomatico";

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const controles = divElement.querySelector("#contenedor-semiAutomaticoRutinas");
  controles.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "cabezal_indexar":
        SemiAutomatico(
          "continuar",
          window.location.hash.split("#/")[1].split("S")[0],
          "semiautomatico"
        );
        break;
      case "carga":
        SemiAutomatico(                                                                           //ver si es un solo boton que hace toda la rutina como en bwa o si son varios botones que cada uno hace una rutina, si es asi tengo que hacer varios utils sino solo usar el de semi y switchear en cada caso de rutina
          "detener",
          window.location.hash.split("#/")[1].split("S")[0],
          "semiautomatico"
        );
        break; 
      case "roscado":
        SemiAutomatico(
          "continuar",
          window.location.hash.split("#/")[1].split("S")[0],
          "semiautomatico"
        );
        break;
      case "descarga":
        SemiAutomatico(
          "continuar",
          window.location.hash.split("#/")[1].split("S")[0],
          "semiautomatico"
        );
        break;
      case "stop":
        SemiAutomatico(
          "continuar",
          window.location.hash.split("#/")[1].split("S")[0],
          "semiautomatico"
        );
        break;
      /*case "refrescar":                                            //boton de refrescar para agregar a futuro
        Graficar("line", "Deformacion", 1, "esc", 1);
        break;*/
    }
  });
  
  return divElement;
};