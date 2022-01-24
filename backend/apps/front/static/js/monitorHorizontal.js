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
window.onload = function() {
   
    //Configuration variables
    var updateInterval = 20 //in ms
    var numberElements = 200;

    //Globals
    var updateCount = 0;

    // Chart Objects
    var xAccelChart = $("#xAccelChart");
    //chart instances & configuration



    var commonOptions = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        legend: {display: false},
        tooltips:{
          enabled: false
        },
    };
    
    var xAccelChartInstance = new Chart(xAccelChart, {
        type: 'line',
        data: {
            datasets: [{
                label: "X Acceleration",
                data: 0,
                fill: false,
                borderColor: '#343e9a',
                borderWidth: 1
            }]
        },
        options: Object.assign({}, commonOptions, {
          title:{
            display: true,
            text: "Acceleration - X",
            fontSize: 18
          },
          
        }),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy',
                        xScale0: {
                            max: 1e4
                        }
                    },
                    zoom: {
                        enabled: true,
                        mode: 'xy'
                    }
                }
            }
        },
       
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

        if(datosWs){
        xAccelChartInstance.data.labels.push(datosWs.husillo_rpm);
        xAccelChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(datosWs.cabezal_pos)});
        if(updateCount > numberElements){
            xAccelChartInstance.data.labels.shift();
            xAccelChartInstance.data.datasets[0].data.shift();
        }
        else updateCount++;
        xAccelChartInstance.update();
        }
      
        
}
}}