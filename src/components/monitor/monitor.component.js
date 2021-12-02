export function Monitorear(dataWs) {
    const componenteMonitor = document.querySelector("#component-monitor");
    // Indicadores
    const statusEjeVertical = document.querySelector("#statusVerticalAxis");
    const statusEjeHorizontal = document.querySelector("#statusFlatAxis");
    const statusPalpador = document.querySelector("#statusTouchProbe");
    const statusCeldaCarga = document.querySelector("#statusStrainGauge");
    const statusGirador = document.querySelector("#statusTurner");
    const statusPresenciaCuchilla = document.querySelector(
      "#statusBladePresence"
    );
    const statusCondicionesIniciales = document.querySelector(
      "#statusInitialConditions"
    );
    const statusSeguroInicial = document.querySelector(
      "#statusSafeInitial"
    );
    const statusParameter = document.querySelector(
      "#statusParameter"
    );
    const homeOk = document.querySelector("#homeOk");
    
    // Tabla de datos
    const fuerzaActual = document.querySelector("#pvFuerza");
    const palpadorActual = document.querySelector("#pvPalpador");
  
    // Maquina de ESTADOS
    const indEstadosV = document.getElementsByClassName("estadoV");
    //const indEstadosH = document.getElementsByClassName("estadoH");
  
    // Datos Eje vertical
    const posicionActualV = document.querySelector("#posVertical");
    const velocidadActualV = document.querySelector("#velVertical");
  
    // Datos Eje Horizontal
    const posicionActualH = document.querySelector("#posHorizontal");
    const velocidadActualH = document.querySelector("#velHorizontal");
  
  
  
    if (dataWs) {
      //Monitor
      fuerzaActual.innerHTML = dataWs.v_fza.toFixed(1);
      palpadorActual.innerHTML = dataWs.v_strain.toFixed(1);
  
      posicionActualV.innerHTML = dataWs.v_pos.toFixed(1);
      velocidadActualV.innerHTML = dataWs.v_vel.toFixed(1);
  
      posicionActualH.innerHTML = dataWs.h_pos.toFixed(1);
      velocidadActualH.innerHTML = dataWs.h_vel.toFixed(1);
    
      
      // Generacion de flag de presencia de cuchilla. Es la combinacion del estatus 1 de digin_0 y digin_1 bit 10 en '1'
      //Cuchilla en mesa
      dataWs.states.ctrl.digin_0.toString(2)[10]=='1' || dataWs.states.ctrl.digin_1.toString(2)[10]=='1' 
        ?statusPresenciaCuchilla.className="bg-success indicadorMon"
        :statusPresenciaCuchilla.className="bg-secondary indicadorMon";
  
  
      //Girador
      dataWs.states.ctrl.digin_0.toString(2)[3] == '1' && dataWs.states.ctrl.digin_1.toString(2)[3] == '1'
      && dataWs.states.ctrl.digin_0.toString(2)[7] == '1' && dataWs.states.ctrl.digin_1.toString(2)[7] == '1'
      && dataWs.states.ctrl.digin_0.toString(2)[5] == '1' && dataWs.states.ctrl.digin_1.toString(2)[5] == '1'
      && dataWs.states.ctrl.digin_0.toString(2)[0] == '1' && dataWs.states.ctrl.digin_1.toString(2)[0] == '1'
      && (dataWs.states.ctrl.digin_0.toString(2)[8] == '1' && dataWs.states.ctrl.digin_1.toString(2)[8] == '1' 
      || dataWs.states.ctrl.digin_0.toString(2)[9] == '1' && dataWs.states.ctrl.digin_1.toString(2)[9] == '1')
        ?statusGirador.className="bg-success indicadorMon"
        :statusGirador.className="bg-danger indicadorMon";
       
  
      //Celda de carga
      let celda
      let fuerzaDelta0negativo = (dataWs.fza_delta_cero)*(-1)
        if (
          dataWs.states.ctrl.digin_0.toString(2)[10]=='0' && dataWs.states.ctrl.digin_1.toString(2)[10]=='0' 
          && ( dataWs.v_fza > dataWs.fza_delta_cero || dataWs.v_fza < fuerzaDelta0negativo )
        ) {
          statusCeldaCarga.className="bg-danger indicadorMon"
          celda = 0
        } else {
          statusCeldaCarga.className="bg-success indicadorMon"
          celda = 1
        }
      
      
      
      //Palpador
      let palpador
      let tol_inf = (dataWs.palp_val_extrem - dataWs.tol_val_extrem)
      let tol_sup = (dataWs.palp_val_extrem + dataWs.tol_val_extrem)
        if (
            dataWs.states.ctrl.digin_0.toString(2)[10]=='0' && dataWs.states.ctrl.digin_1.toString(2)[10]=='0' 
            && ( dataWs.v_strain < tol_inf || dataWs.v_strain > tol_sup)
        ) {
          statusPalpador.className="bg-danger indicadorMon"
          palpador=0
        } else {
          statusPalpador.className="bg-success indicadorMon"
          palpador=1
        }
    
  
        
  
      //Eje vertical
      let vertical_drv_fbk
      let ACDP_FLAGSTAT_DrvFbk_Ready
      let ACDP_FLAGSTAT_DrvFbk_Enabled
      let ACDP_FLAGSTAT_DrvFbk_ZeroSettled
  
      vertical_drv_fbk = dataWs.states.vertical.drv_fbk.toString(2).split('').reverse()
      
      ACDP_FLAGSTAT_DrvFbk_Ready = vertical_drv_fbk [0]
      ACDP_FLAGSTAT_DrvFbk_Enabled = vertical_drv_fbk [1]
      ACDP_FLAGSTAT_DrvFbk_ZeroSettled = vertical_drv_fbk [8]
      
      if (ACDP_FLAGSTAT_DrvFbk_Ready == 1 && ACDP_FLAGSTAT_DrvFbk_Enabled == 1 && ACDP_FLAGSTAT_DrvFbk_ZeroSettled == 1) 
      {
        statusEjeVertical.className = "bg-success indicadorMon"
      } else {
        statusEjeVertical.className = "bg-secondary indicadorMon"
      }
    //console.log("drv_fbk: ", ACDP_FLAGSTAT_DrvFbk_Ready, ACDP_FLAGSTAT_DrvFbk_Enabled, ACDP_FLAGSTAT_DrvFbk_ZeroSettled);
    //console.log("drv_fbk: ", dataWs.states.horizontal.drv_fbk.toString(2).split(''), dataWs.states.horizontal.drv_fbk) 
    
  /*  # Flags de status
      # ACDP_FLAGSTAT_DrvFbk_Ready            = 1 << 0
      # ACDP_FLAGSTAT_DrvFbk_Enabled          = 1 << 1
      # ACDP_FLAGSTAT_DrvFbk_Fault            = 1 << 2
      # ACDP_FLAGSTAT_DrvFbk_PositiveOt       = 1 << 3
      # ACDP_FLAGSTAT_DrvFbk_NegativeOt       = 1 << 4
      # ACDP_FLAGSTAT_DrvFbk_HomeSwitch       = 1 << 5
      # ACDP_FLAGSTAT_DrvFbk_HomingEndedOk    = 1 << 6
      # ACDP_FLAGSTAT_DrvFbk_HomingError      = 1 << 7
      # ACDP_FLAGSTAT_DrvFbk_ZeroSettled      = 1 << 8
      # ACDP_FLAGSTAT_DrvFbk_UnknownZero      = 1 << 9
      # ACDP_FLAGSTAT_DrvFbk_PosDec           = 1 << 10
      # ACDP_FLAGSTAT_DrvFbk_TimeOvPulso      = 1 << 11 */ 
      
    
      //Eje horizontal
      let horizontal_drv_fbk
      let ACDP_FLAGSTAT_DrvFbk_Ready_horizontal
      let ACDP_FLAGSTAT_DrvFbk_Enabled_horizontal
      let ACDP_FLAGSTAT_DrvFbk_ZeroSettled_horizontal
  
      horizontal_drv_fbk = dataWs.states.horizontal.drv_fbk.toString(2).split('').reverse()
      
      ACDP_FLAGSTAT_DrvFbk_Ready_horizontal = horizontal_drv_fbk [0]
      ACDP_FLAGSTAT_DrvFbk_Enabled_horizontal = horizontal_drv_fbk [1]
      ACDP_FLAGSTAT_DrvFbk_ZeroSettled_horizontal = horizontal_drv_fbk [8]
      
      if (ACDP_FLAGSTAT_DrvFbk_Ready_horizontal == 1 
      && ACDP_FLAGSTAT_DrvFbk_Enabled_horizontal == 1 
      && ACDP_FLAGSTAT_DrvFbk_ZeroSettled_horizontal == 1) 
      {
        statusEjeHorizontal.className = "bg-success indicadorMon"
      } else {
        statusEjeHorizontal.className = "bg-secondary indicadorMon"
      }
  
  
      // es el botón verde que se ve en referenciar
      if (homeOk) {
        if (
        ACDP_FLAGSTAT_DrvFbk_ZeroSettled_horizontal == 1 &&
        ACDP_FLAGSTAT_DrvFbk_ZeroSettled == 1
        && palpador == 1
        && celda == 1
      ) {
        homeOk.className = "bg-success rounded-pill text-white text-center p-3";
      } else {
        homeOk.className = "bg-secondary rounded-pill text-white text-center p-3";
      }
      }
  
  
  
  
     //Safe/initial
    dataWs.states.vertical.estado.toString(2)=='0' && dataWs.states.horizontal.estado.toString(2)=='0'
      ?statusSeguroInicial.className = "bg-secondary indicadorMonSafe"
      :statusSeguroInicial.className = "bg-success   indicadorMonSafe"
        
     
    //console.log(dataWs);  
    
    
  
  
      
      
    
  }
  }
  