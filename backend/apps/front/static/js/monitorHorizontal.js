

var monitor = null;
var monitorHorizontal = null;

    const socket = new WebSocket("ws://127.0.0.1:8000/ws/front/");
    socket.addEventListener("open", function (event) {
        socket.send(
          JSON.stringify({
            message: "datos",      
          })
        );
    });
    // Escucha cierre de WebSocket
    socket.onclose = function (event) {
        window.location.reload();
      };
    
window.addEventListener("hashchange", () => {                  //cuando tocas f5
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});

socket.onmessage = function (event) {
  const datosWs = JSON.parse(event.data);
  

  // Tabla de datos
  const rpmActual = document.querySelector("#frRPMH");
  const torqueActual = document.querySelector("#fTorqueH");

  // Datos Eje vertical
  const posicionActualV = document.querySelector("#posVerticalH");
  const velocidadActualV = document.querySelector("#velVerticalH");

  // Datos Eje Horizontal
  const posicionActualH = document.querySelector("#posHorizontalH");
  const velocidadActualH = document.querySelector("#velHorizontalH");

  //Grafico
  const contenedorGrafico = document.querySelector("#component-grafico-roscado");

  if (datosWs) {
    //Monitor
    rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);

    posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);

    posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);


    
    var ctx = document.getElementById("component-grafico-roscado").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Tokyo",	"Mumbai",	"Mexico City",	"Shanghai",	"Sao Paulo",	"New York",	"Karachi","Buenos Aires",	"Delhi","Moscow"],
            datasets: [{
                label: 'Series 1', // Name the series
                data: [500,	50,	2424,	14040,	14141,	4111,	4544,	47,	5555, 6811], // Specify the data values array
                fill: false,
                borderColor: '#2196f3', // Add custom color border (Line)
                backgroundColor: '#FFFFFF', // Add custom color background (Points and Fill)
                borderWidth: 1 // Specify bar border width
            }]},
        options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
        }
    });
    
    
    
}
}