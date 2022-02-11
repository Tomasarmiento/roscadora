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

    //Modelo Cupla
    for(let i=1; i <= 3; i++){
        let btn_id = 'selCuple' + i;
        btn = document.getElementById(btn_id);
        csrf_token = btn.getAttribute('token');
        btn.addEventListener('click', (e) => {
            btn.className = "badge lg-badge badge-pill badge-success indLargo";
            let url = "http://localhost:8000/parametros/";
            let params = "part_model=" + i + "&csrfmiddlewaretoken=" + csrf_token;
        
            let xhr = new XMLHttpRequest();
        
            xhr.open("POST", url, true);
        
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        
            xhr.send(params);

            location.reload(true)
        });
    }

});