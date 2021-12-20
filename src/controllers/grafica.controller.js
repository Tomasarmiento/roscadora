import views from "../views/grafica.html";
import graficaFuerza from "../components/graficos/graficaFuerza.component.html";
import graficaDeformacion from "../components/graficos/graficaDeformacion.component.html";
import { Graficar2, Graficar_end2, FilterDates} from "../statics/utils/generarGraficas";



export default async () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  const graficoEscaneo = divElement.querySelector("#component-grafico-escaneo");
  graficoEscaneo.innerHTML = graficaDeformacion;

  const graficoEnderezado = divElement.querySelector(
    "#component-grafico-enderezado"
  );
  graficoEnderezado.innerHTML = graficaFuerza;

  /*const tituloPagina = document.getElementById("tituloPagina");
  tituloPagina.innerHTML = "GRÁFICA";
  tituloPagina.className = "h3";*/

  const idValue = divElement.querySelector("#idSearch");
  const iterationValue = divElement.querySelector("#iterationSearch");
  const dateValue = divElement.querySelector("#dateSearch");

  const filtro = divElement.querySelector("#contenedor-imputBox");
  const limpiar = divElement.querySelector("#contenedor-imputBox");

  filtro.addEventListener("click", (e) => {
    switch (e.target.id) { case "graficado":
    Graficar_end2("line", "Fuerza", idValue.value, "end", iterationValue.value);
    Graficar2("line", "Deformacion", idValue.value, "esc", iterationValue.value);
    break;
    }
  });

  

  function sampleFunction() {
    location.reload(true);
  }
  limpiar.addEventListener("click", (e) => {
    switch (e.target.id) { case "limpiado":
    sampleFunction();  
  }
});


filtro.addEventListener("click", (e) => { 
  switch (e.target.id) { case "filtrado":
  FilterDates(dateValue.value, "part_ids");
   
}
});

return divElement;
};