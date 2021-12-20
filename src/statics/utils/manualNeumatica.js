
class Neumatica {
    constructor(actuador, comando) {
      this.actuador = actuador;
      this.comando = comando;
    }
    async request() {
      const response = await fetch(`${env.URL_BASE}menu/manual/`, {
        method: "post",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({
          menu: "neumatica",
          actuador: this.actuador,
          comando: this.comando,
        }),
      });
    }
}

export async function ComandosNeumatica(actuador, comando) {                 // 00! (horizontal,on) Le pasa
    switch (actuador) {
      case "horizontal_carga":
        const peticionHorCarg = new Neumatica(actuador, comando);
        peticionHorCarg.request();
        break;
  
      case "pinza_carga":
        const peticionPinzaCarg = new Neumatica(actuador, comando);
        peticionPinzaCarg.request();
        break;
  
      case "vertical_carga":
        const peticionVerticalCarg = new Neumatica(actuador, comando);
        peticionVerticalCarg.request();
        break;
  
      case "giro_carga":
        const peticionGiroCarg = new Neumatica(actuador, comando);
        peticionGiroCarg.request();
        break;
    
      case "horizontal_descarga":
        const peticionHorDesc = new Neumatica(actuador, comando);
        peticionHorDesc.request();
        break;
  
      case "pinza_descarga":
        const peticionPinzaDesc = new Neumatica(actuador, comando);
        peticionPinzaDesc.request();
        break;
  
      case "vertical_br":
        const peticionVerticalBr = new Neumatica(actuador, comando);
        peticionVerticalBr.request();
        break;
  
      case "giro_descarga":
        const peticionGiroDesc = new Neumatica(actuador, comando);
        peticionGiroDesc.request();
        break;
  
      case "horizontal_br":
        const peticionHorBr = new Neumatica(actuador, comando);
        peticionHorBr.request();
        break;
  
      case "pinza_br":
        const peticionPinzaBr = new Neumatica(actuador, comando);
        peticionPinzaBr.request();
        break;
    
      case "clampeo":
        const peticionClampeo = new Neumatica(actuador, comando);
        peticionClampeo.request();
        break;
  
      case "boquilla1":
        const peticionBoq1 = new Neumatica(actuador, comando);
        peticionBoq1.request();
        break;
  
      case "boquilla2":
        const peticionBoq2 = new Neumatica(actuador, comando);
        peticionBoq2.request();
        break;
  
      case "boquilla3":
        const peticionBoq3 = new Neumatica(actuador, comando);
        peticionBoq3.request();
        break;
  
      case "acopla_soluble":
        const peticionAcoplaSol = new Neumatica(actuador, comando);
        peticionAcoplaSol.request();
        break;
  
      case "bomba_soluble":
        const peticionBombaSol = new Neumatica(actuador, comando);
        peticionBombaSol.request();
        break;
    }
  }