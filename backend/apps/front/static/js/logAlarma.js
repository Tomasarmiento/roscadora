window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    let btn_servo1 = document.getElementById('servo1');

        btn_servo1.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });

    let btn_servo2 = document.getElementById('servo2');

        btn_servo2.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });

    let btn_servo3 = document.getElementById('servo3');

        btn_servo3.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";

            let xhr = new XMLHttpRequest();

            xhr.open("POST", url, true);

            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xhr.send();
        });
});