
var monitor = null;



    
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
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

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

    
});

console.log('levanta semiautomatico.js');




