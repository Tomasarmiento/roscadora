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


});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    let btn_cabezal = document.getElementById('cabezal_indexar');
    let btn_carga = document.getElementById('carga');
    let btn_roscado = document.getElementById('roscado');
    let btn_descarga = document.getElementById('descarga');
    
    btn_cabezal.addEventListener('click', (e) => {
        let routine = btn_cabezal.getAttribute('rtn');
        startRoutine(routine);
    });

    btn_carga.addEventListener('click', (e) => {
        let routine = btn_carga.getAttribute('rtn');
        startRoutine(routine);
    });

    btn_roscado.addEventListener('click', (e) => {
        let routine = btn_roscado.getAttribute('rtn');
        startRoutine(routine), xAccelChartInstance.destroy();
    });

    btn_descarga.addEventListener('click', (e) => {
        let routine = btn_descarga.getAttribute('rtn');
        startRoutine(routine);
    });
    monitor = document.querySelector("#component-monitor");


    function startRoutine(routine){
        let url = "http://localhost:8000/control/semiautomatico/";
        let params = "routine=" + routine;
    
        // var params = "lorem=ipsum&name=alpha";
        let xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
    
        //Send the proper header information along with the request
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
        xhr.send(params);
    }
    cuadroDeTextoIndex = document.querySelector("#terminalDeTexto");
    if (sessionStorage.getItem("mensajes") && cuadroDeTextoIndex) {
        console.log('aca');
        let ul = document.getElementById("cuadroMensajes");
        const listaMensajes = sessionStorage.getItem("mensajes").split(",");
        for (let i = 0; i < listaMensajes.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;");
            li.innerHTML = listaMensajes[i];
            ul.appendChild(li);
        }
    }

    cuadroDeErrores = document.querySelector("#terminalDeTexto");
    if (sessionStorage.getItem("mensajesError") && cuadroDeErrores) {
        console.log('aca');
        let ul = document.getElementById("cuadroMensajes");
        const listaMensajes = sessionStorage.getItem("mensajesError").split(",");
        for (let i = 0; i < listaMensajes.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;");
            li.innerHTML = listaMensajes[i];
            ul.appendChild(li);
        }
    }
    
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
    // const btnSemiContainer = document.querySelector("#contenedor-semiAutomaticoRutinas");
   
    var commonOptions = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                },
            }],
            xAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        backgroundColor: '#ffffff73',
        legend: {display: true},
        tooltips:{
          enabled: false
        },
    };
    
    var xAccelChartInstance = new Chart(xAccelChart, {
        type: 'line',
        data: {
            datasets: [{
                label: "Torque",
                data: 0,
                pointRadius: 0.5,
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
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Torque'
                    },   
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Posición'
                    },
                    type: 'time',
                    time: {
                            unit: 'second',
                            
                            displayFormats: {
                                second: 'mm:ss'
                              }
                    },
                    displayFormats: {
                        second: 'ss:SSS'
                      }
                }],
               
            },
            responsive: true,
            
            maintainAspectRatio: false,
            backgroundColor: '#ffffff73',
            plugins: {
                legend:  false,
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy',
                        xScale0: {
                            max: 1e4
                        }, 
                    },
                    zoom: {
                        enabled: true,
                        mode: 'xy'
                    },
                    pinch: {
                        enabled: true,
                    },
                    sensitivity:0.1,
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
    let btn_reset_zoom = document.getElementById('resetLittleZoom');
    btn_reset_zoom.addEventListener('click', (e) => {
        xAccelChartInstance.resetZoom();
    });
    
    // btnContainer.addEventListener("click", (e) => {
    // switch (e.target.id) {
    //   case "resetZoom":
    //     xAccelChartInstance.resetZoom()
    // break;
    //   case "destroy":
    //     xAccelChartInstance.destroy();
    // break;
    // }
    // });

    // btnSemiContainer.addEventListener("click", (e) => {
    //     switch (e.target.id) {
    //       case "roscado":
    //         xAccelChartInstance.destroy();
    //     break;
    //     }
    // });

    

    function InsertarTexto(datosWs) {
        var ul = document.getElementById("cuadroMensajes");
        for (let i = 0; i < datosWs.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;" );
            li.innerHTML = datosWs[i];
            ul.prepend(li);
        }
    }

    function InsertarTextoErrores(datosWs) {
        var ul = document.getElementById("cuadroMensajesErrores");
        for (let i = 0; i < datosWs.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;" );
            li.innerHTML = datosWs[i];
            ul.prepend(li);
        }
    }

   
    
    
    var listaMensajes = []; 
    var listaMensajesErrores = [];
    socket.onmessage = function (event) {
     const datosWs = JSON.parse(event.data);

    if (datosWs.mensajes_log.length > 0) {
        listaMensajes.push(datosWs.mensajes_log);
        sessionStorage.setItem("mensajes", listaMensajes);
        InsertarTexto(datosWs.mensajes_log);
    };
    if (datosWs.mensajes_error.length > 0) {
        listaMensajesErrores.push(datosWs.mensajes_error);
        sessionStorage.setItem("mensajes", listaMensajesErrores);
        InsertarTextoErrores(datosWs.mensajes_error);
    };



        if(datosWs){
            xAccelChartInstance.data.labels.push(new Date());            //(datosWs.cabezal_pos).toFixed(1);
            xAccelChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(datosWs.husillo_torque).toFixed(1)});
        if(updateCount > numberElements){
            xAccelChartInstance.data.labels;
            xAccelChartInstance.data.datasets[0].data;
        }
        else updateCount++;
        xAccelChartInstance.update();
        }
      
        
}
};




