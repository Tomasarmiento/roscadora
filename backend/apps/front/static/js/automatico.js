var data = []
var monitor = null;




document.addEventListener("DOMContentLoaded", (e) => {
    let btn_continue = document.getElementById('continue');

    btn_continue.addEventListener('click', (e) => {
        let url = "http://localhost:8000/control/auto/";

        let xhr = new XMLHttpRequest();

        xhr.open("POST", url, true);

        //Send the proper header information along with the request
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xhr.send();
    });

    
   
});

console.log('levanta automatico.js');