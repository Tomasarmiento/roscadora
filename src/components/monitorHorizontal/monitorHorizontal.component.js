export function MonitorearBanner(dataWs) {
    const componenteMonitor = document.querySelector(
      "#component-monitor-horizontal"
    );
    // Tabla de datos
    const rpmActual = document.querySelector("#frRPM");
    const torqueActual = document.querySelector("#fTorque");
  
    // Datos Eje vertical
    const posicionActualV = document.querySelector("#posVertical");
    const velocidadActualV = document.querySelector("#velVertical");
  
    // Datos Eje Horizontal
    const posicionActualH = document.querySelector("#posHorizontal");
    const velocidadActualH = document.querySelector("#velHorizontal");
  
    rpmActual.innerHTML = dataWs.v_rpm.toFixed(0);                    //ver decimales  
    torqueActual.innerHTML = dataWs.v_torque.toFixed(0);                
  
    posicionActualV.innerHTML = dataWs.v_pos.toFixed(0);
    velocidadActualV.innerHTML = dataWs.v_vel.toFixed(0);
  
    posicionActualH.innerHTML = dataWs.h_pos.toFixed(0);
    velocidadActualH.innerHTML = dataWs.h_vel.toFixed(0);
  }
  