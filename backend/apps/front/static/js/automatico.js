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
    let btn_continue = document.getElementById('continue');
    let btn_cancel = document.getElementById('cancel');
    
        btn_continue.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });
    monitor = document.querySelector("#component-monitor");


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
        let ul = document.getElementById("cuadroMensajesErrores");
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
    var configuration = {
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
    }


    var xAccelChartInstance = new Chart(xAccelChart, configuration);
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
    var delete_graph = true;
    socket.onmessage = function (event) {
     const datosWs = JSON.parse(event.data);

    if (datosWs.mensajes_log) {
        listaMensajes.push(datosWs.mensajes_log);
        sessionStorage.setItem("mensajes", listaMensajes);
        InsertarTexto(datosWs.mensajes_log);
    };
    if (datosWs.mensajes_error) {
        listaMensajesErrores.push(datosWs.mensajes_error);
        sessionStorage.setItem("mensajesError", listaMensajesErrores);
        InsertarTextoErrores(datosWs.mensajes_error);
    };

    // Tabla de datos
    const rpmActual = document.querySelector("#frRPM");
    const torqueActual = document.querySelector("#fTorque");

    // Datos Eje vertical
    const posicionActualV = document.querySelector("#posVertical");
    const velocidadActualV = document.querySelector("#velVertical");

    // Datos Eje Horizontal
    const posicionActualH = document.querySelector("#posHorizontal");
    const velocidadActualH = document.querySelector("#velHorizontal");


    //Cabezal
    const cabezal = document.querySelector("#statusHead")
    //Eje Lineal
    const ejeLineal = document.querySelector("#statusLinealAxis")
    //Descarga
    const descarga = document.querySelector("#statusDownloader");
    //Carga
    const carga = document.querySelector("#statusLoader");
    //Indexar
    const indexar = document.querySelector("#statusIndex");
    //Roscado
    const roscado = document.querySelector("#statusRoscado")
    //Safe
    const safe = document.querySelector("#statusSafe");

    

    if(datosWs){
        if(delete_graph == true){
             
             function sleep (time) {
                 return new Promise((resolve) => setTimeout(resolve, time));              //time sleep
                 }
                 sleep(1800).then(() => {
                    xAccelChartInstance.data.datasets[0].data = []

                    
                });
                delete_graph = false;
                console.log('aca');
            }
            
            console.log(xAccelChartInstance.data.datasets[0].data);



        xAccelChartInstance.data.labels.push(new Date());            //(datosWs.cabezal_pos).toFixed(1);
        xAccelChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(datosWs.husillo_torque).toFixed(1)});
        
        if(updateCount > numberElements){
            xAccelChartInstance.data.labels;
            xAccelChartInstance.data.datasets[0].data;
        }
        else updateCount++;
        xAccelChartInstance.update();
        }

       
       

        
          
    if(datosWs){
    //Monitor
    rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);

    posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);

    posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);

    // //cabezal
    // if (datosWs.estado_eje_carga == 'initial'){
    //   (cabezal.className = "bg-success indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Initial') 
    //   }

    //   else if (datosWs.estado_eje_carga == 'homing'){
    //   (cabezal.className = "bg-warning indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Homming')
    //   }

    // else (cabezal.className = "bg-secondary indicadorMon");
    
    
    // //eje lineal
    // if (datosWs.estado_eje_avance == 'initial'){
    //   (ejeLineal.className = "bg-success indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Initial') 
    //   }

    //   else if (datosWs.estado_eje_avance == 'homing'){
    //   (ejeLineal.className = "bg-warning indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Homming')
    //   }

    // else (ejeLineal.className = "bg-secondary indicadorMon");
     
     


    //descarga
    // datosWs.remote_outputs[1].encender_bomba_hidraulica == true 
    //  && datosWs.remote_inputs[1].clampeo_plato_expandido == true
    //  && datosWs.remote_inputs[0].puntera_descarga_contraida == true
    //  && datosWs.remote_inputs[0].brazo_descarga_expandido == true
    //  && datosWs.remote_inputs[0].boquilla_descarga_expandida == true
    //  && datosWs.remote_inputs[1].cupla_por_tobogan_descarga == true
    //  && datosWs.remote_inputs[1].pieza_en_boquilla_descarga == true
    //  && datosWs.remote_inputs[1].horiz_pinza_desc_contraido == true
    //  && datosWs.remote_inputs[1].vert_pinza_desc_contraido == true
    //  && datosWs.remote_inputs[0].pinza_descargadora_abierta == true && datosWs.remote_inputs[0].pinza_descargadora_cerrada == false
    // ? (descarga.className = "bg-success indicadorMon")
    // : (descarga.className = "bg-secondary indicadorMon");


    // //carga
    // datosWs.remote_outputs[1].encender_bomba_hidraulica == true
    //  && datosWs.remote_inputs[1].clampeo_plato_expandido == true
    //  && datosWs.remote_inputs[0].vertical_carga_contraido == true
    //  && datosWs.remote_inputs[0].puntera_carga_expandida == false && datosWs.remote_inputs[0].puntera_carga_contraida == true
    //  && datosWs.remote_inputs[0].brazo_cargador_expandido == true && datosWs.remote_inputs[0].brazo_cargador_contraido == false
    //  && datosWs.remote_inputs[0].boquilla_carga_expandida == true
    //  && datosWs.remote_inputs[1].presencia_cupla_en_cargador == true
    //  && datosWs.remote_inputs[1].pieza_en_boquilla_carga == true
    // ? (carga.className = "bg-success indicadorMon")
    // : (carga.className = "bg-secondary indicadorMon");

    // //indexar
    // datosWs.remote_inputs[1].clampeo_plato_contraido == false && datosWs.remote_inputs[1].clampeo_plato_expandido == true
    //  && datosWs.remote_inputs[1].acople_lubric_contraido == true
    //  && datosWs.remote_inputs[0].puntera_descarga_expandida == false && datosWs.remote_inputs[0].puntera_descarga_contraida == true
    //  && datosWs.remote_inputs[0].puntera_carga_expandida == false && datosWs.remote_inputs[0].puntera_carga_contraida == true
    //  && datosWs.avance_pos.toFixed(1) >= datosWs.posicion_de_inicio
    //  ? (indexar.className = "bg-success indicadorMon")
    //  : (indexar.className = "bg-secondary indicadorMon");


    // //roscado
    // datosWs.remote_outputs[1].encender_bomba_hidraulica == true
    //  && datosWs.remote_inputs[1].clampeo_plato_contraido == false && datosWs.remote_inputs[1].clampeo_plato_expandido == true
    //  && datosWs.estado_eje_avance == 'initial'
    //  && datosWs.cabezal_enable == false
    //  && datosWs.avance_pos.toFixed(1) == datosWs.posicion_de_inicio
    //  ? (roscado.className = "bg-success indicadorMon")
    //  : (roscado.className = "bg-secondary indicadorMon");
     

    //  //safe
    // (datosWs.estado_eje_carga == 'safe')
    //  && (datosWs.estado_eje_avance == 'safe')
    //  && (datosWs.estado_eje_giro == 'safe')
    //  ?  (safe.className = "bg-danger indicadorMon")
    //  :  (safe.className = "bg-secondary indicadorMon");

    
      
    }
}};

