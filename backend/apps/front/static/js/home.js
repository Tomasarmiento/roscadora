window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    let btn_modoSafe = document.getElementById('modoSafe'); 
    
        btn_modoSafe.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/safe/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });

});