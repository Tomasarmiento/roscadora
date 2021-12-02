import views from "../views/semiautomatico.html";








export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

  
  

  


  return divElement;
};