var data = []
var monitor = null;

    
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
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

    
   
});

console.log('levanta automatico.js');
