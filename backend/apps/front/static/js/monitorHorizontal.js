var data = []
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
const totalDuration = 10000;
    const delayBetweenPoints = totalDuration / data.length;
    const previousY = (ctx) => ctx.index === 0 
    ? ctx.chart.scales.y.getPixelForValue(100) 
    : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;

window.onload = function() {

   

    //Configuration variables
    var updateInterval = 20 //in ms
    var numberElements = 200;

    //Globals
    var updateCount = 0;

    // Chart Objects
    var xAccelChart = $("#xAccelChart");
    //chart instances & configuration


    const btnContainer = document.querySelector("#resetZoomDiv");
   


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
        backgroundColor: '#ffffff73',
        legend: {display: false},
        tooltips:{
          enabled: false
        },
    };
    
    var xAccelChartInstance = new Chart(xAccelChart, {
        type: 'line',
        data: {
            datasets: [{
                label: "cabezal_pos",
                data: 0,
                fill: false,
                borderColor: '#00aeef',
                backgroundColor: 'blue',
                borderWidth: 2
            }]
        },
        options: Object.assign({}, commonOptions, {
          title:{
            display: true,
            text: "cabezal_pos",
            fontSize: 18,
            backgroundColor: '#ffffff73',
          },
          
        }),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            backgroundColor: '#ffffff73',
            plugins: {
                legend: false,
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
                    },
                    pinch: {
                        enabled: true,
                    },
                    legend: false,
                }
            },
            animation:{
                x: {
                    type: 'number',
                    easing: 'linear',
                    duration: delayBetweenPoints,
                    from: NaN, // the point is initially skipped
                    delay(ctx) {
                    if (ctx.type !== 'data' || ctx.xStarted) {
                        return 0;
                    }
                    ctx.xStarted = true;
                    return ctx.index * delayBetweenPoints;
                    }
                },
                y: {
                    type: 'number',
                    easing: 'linear',
                    duration: delayBetweenPoints,
                    from: previousY,
                    delay(ctx) {
                    if (ctx.type !== 'data' || ctx.yStarted) {
                        return 0;
                    }
                    ctx.yStarted = true;
                    return ctx.index * delayBetweenPoints;
                    }
                }
            },
        }
    });
   

    
   
    btnContainer.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "resetZoom":
        xAccelChartInstance.resetZoom()
    break;
    }
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
        xAccelChartInstance.data.labels.push(datosWs.husillo_rpm).toFixed(2);
        xAccelChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(datosWs.cabezal_pos).toFixed(2)});
        if(updateCount > numberElements){
            xAccelChartInstance.data.labels.shift();
            xAccelChartInstance.data.datasets[0].data.shift();
        }
        else updateCount++;
        xAccelChartInstance.update();
        }
      
        
}
}}