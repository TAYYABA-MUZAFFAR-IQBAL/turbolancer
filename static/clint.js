function isElementOverflowingX(element) {
    const scrollWidth = element.scrollWidth;
    const clientWidth = element.clientWidth;
    return scrollWidth > clientWidth;
  }
  
  function zoomContentX(element) {
    const isOverflowingX = isElementOverflowingX(element);
  
    if (isOverflowingX) {
      const scrollWidth = element.scrollWidth;
      const clientWidth = element.clientWidth;
      const zoomLevel = clientWidth / scrollWidth;
  
      const childElements = element.children;
      for (let i = 0; i < childElements.length; i++) {
        const child = childElements[i];
        child.style.transform = `scale(${zoomLevel})`;
        child.style.transformOrigin = 'left top';
        child.style.fontSize = `${1 / zoomLevel * 100}%`;
      }
    } else {
      const childElements = element.children;
      for (let i = 0; i < childElements.length; i++) {
        const child = childElements[i];
        child.style.transform = 'none';
        child.style.transformOrigin = 'unset';
        child.style.fontSize = '100%';
      }
    }
  }
  
  // Example usage
  
  
  
          let scrollDirection = null;
  
  window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
      con = document.querySelector('.tabular_parent')
    if (currentScroll > scrollDirection || scrollDirection === null) {
      con.style.top = '90px'
    } else {
      con.style.top = '80vh'
    }
  
    scrollDirection = currentScroll;
  });
        function _(cookieName) {
          var expirationDate = new Date(0); // Create a Date object set to the epoch time (January 1, 1970)
          var formattedDate = expirationDate.toUTCString(); // Get the UTC string representation of the date
  
          document.cookie = `${cookieName}=; expires=${formattedDate}; path=/;`;
        }
  
        document
          .getElementById("deleteCookieButton")
          .addEventListener("click", function () {
            list = ["ideo", "emalo", "deno", "tp"];
            for (i = 0; i <= list.length; i++) {
              _(list[i]);
            }
            window.location.reload();
          });
  
        function select(x) {
          function doit(x) {
            document
              .querySelectorAll(".upload_job_if, .getsearved, .proj")
              .forEach((element) => {
                element.style.opacity = "0";
                element.style.display = "none";
              });
  
            document.querySelectorAll(".tab").forEach((tab) => {
              tab.querySelectorAll("span").forEach((element) => {
                element.classList.remove("active");
              });
            });
            const dataAttr = x.getAttribute("data");
  
            x.classList.add("active");
            document.querySelectorAll(".tab").forEach((tab) => {
              tab
                .querySelectorAll(`[data = '${dataAttr}']`)
                .forEach((element) => {
                  element.classList.add("active");
                });
            });
  
            switch (dataAttr) {
              case "job":
                document.querySelector(".upload_job_if").style.display = "block";
                document.querySelector(".upload_job_if").style.opacity = "1";
                break;
              case "service":
                document.querySelector(".getsearved").style.display = "block";
                document.querySelector(".getsearved").style.opacity = "1";
                break;
              case "projects":
                document.querySelector(".proj").style.display = "block";
                document.querySelector(".proj").style.opacity = "1";
                break;
              default:
                break;
            }
          }
  
          if (!document.startViewTransition) {
            doit(x);
            return;
          }
  
          // With View Transitions:
          document.startViewTransition(() => doit(x));
        }
        function openNav() {

          if (!(window.innerWidth < 1220)) {
            document
              .getElementById("full_page")
              .removeEventListener("click", closeNav);
  
            document.getElementById("Sidenav").classList.add('opend');
            document.getElementById("Sidenav").style.width = "322px";
            document.getElementById("Sidenav").style.opacity = "1";
            document.getElementById("Sidenav").style.transformOrigin = "left";
  
            document.getElementById("Sidenav").style.transform = "scalex(1)";
            document.getElementById("full_page").style.width =
              "calc(100% - 322px)";
            document.getElementById("nav1").style.width =
              "calc(100% - 322px)";
              if (!document.querySelector('nav.scrolled')){
                      document.getElementById("tabular_parent").style.width ="calc(98% - 322px)";}
              else{
                  document.getElementById("tabular_parent").style.width ="calc(100% - 322px)";}
  
              
              document.getElementById("full_page").style.filter = "brightness(100%)";
              document.getElementById("nav1").style.filter = "brightness(100%)";
              document.getElementById("tabular_parent").style.filter = "brightness(100%)";
  
            document.getElementById("Sidenav").style.marginLeft = "0px";
          } else {
            document
              .getElementById("full_page")
              .removeEventListener("click", closeNav);
              document.getElementById("Sidenav").classList.add('opend')
            document.getElementById("Sidenav").style.width = "322px";
            document.getElementById("Sidenav").style.opacity = "1";
  
            document.getElementById("Sidenav").style.transformOrigin = "left";
  
            document.getElementById("Sidenav").style.transform = "scalex(1)";
  
            document.getElementById("Sidenav").style.zIndex = "9999999999";
            document.getElementById("Sidenav").style.marginLeft = "0px";
  
            document.getElementById("full_page").style.filter = "brightness(75%)";
            document.getElementById("nav1").style.filter = "brightness(75%)";
            document.getElementById("tabular_parent").style.filter = "brightness(75%)";
            setTimeout(() => {
              document
                .getElementById("full_page")
                .addEventListener("click", closeNav);
            }, 200);
          }
        }
  
        function closeNav() {
          document
            .getElementById("full_page")
            .removeEventListener("click", closeNav);
            document.getElementById("Sidenav").classList.remove('opend')
          document.getElementById("Sidenav").style.transform = "scalex(0)";
          document.getElementById("Sidenav").style.marginLeft = "-3px";
          document.getElementById("Sidenav").style.opacity = "0";
  
          document.getElementById("Sidenav").style.transformOrigin = "left";
  
          document.getElementById("full_page").style.width = "100%";
          document.getElementById("nav1").style.width = "100%";
          document.getElementById("full_page").style.filter = "brightness(100%)";
          document.getElementById("nav1").style.filter = "brightness(100%)";
          document.getElementById("tabular_parent").style.filter = "brightness(100%)";
          if (!document.querySelector('nav.scrolled')){
                      document.getElementById("tabular_parent").style.width ="98%";}
              else{
                  document.getElementById("tabular_parent").style.width ="100%";}
        }
        const contentElement = document.querySelector('nav');
  zoomContentX(contentElement);
        window.addEventListener("resize", function () {
          const contentElement = document.querySelector('nav');
  zoomContentX(contentElement);
          scrollFunction()
          if (window.innerWidth < 1220) {
              
              document.getElementById("Sidenav").classList.remove('opend')
  
            document.getElementById("Sidenav").style.transform = "scalex(0)";
            document.getElementById("Sidenav").style.transformOrigin = "left";
            document.getElementById("Sidenav").style.opacity = "0";
  
            document.getElementById("Sidenav").style.marginLeft = "-3px";
  
            document.getElementById("full_page").style.filter = "brightness(100%)";
              document.getElementById("nav1").style.filter = "brightness(100%)";
              document.getElementById("tabular_parent").style.filter = "brightness(100%)";
              if (document.querySelector("nav.scrolled") ){
              document.querySelector(".tabular_parent").style.width = per(document.querySelector("nav"),1)+'px'
              document.getElementById("tabular_parent").style.right = "0%";
  
          }
              else{
                  document.querySelector(".tabular_parent").style.width = per(document.querySelector("nav"),9)+'px';
                  document.getElementById("tabular_parent").style.right = "1%";
  
              }
  
            document.getElementById("full_page").style.width = "100%";
            document.getElementById("nav1").style.width = "100%";
            scrollFunction()
  
          }
        });
  
    
        document.addEventListener("DOMContentLoaded", function () {
          let imageCount;
          const element = document.querySelector(".hero");
          let currentGradient = 1;
          let count = 3;
          function loadImageAsBase64(url, callback) {
            fetch(url)
              .then((response) => response.blob())
              .then((blob) => {
                const reader = new FileReader();
                reader.onload = () => {
                  const base64Data = reader.result.split(",")[1];
                  callback(base64Data);
                };
                reader.readAsDataURL(blob);
              })
              .catch((error) => {
                toast('d','Error: Cannot load image',20)

                console.error(`Error loading image from ${url}: ${error}`);
                callback(null);
              });
          }
          const base64Array = [];
          function convertImagesToBase64(imageLinks, callback) {
            let completed = 0;
  
            for (let i = 0; i < imageLinks.length; i++) {
              loadImageAsBase64(imageLinks[i], (base64Data) => {
                if (base64Data !== null) {
                  // Remove any additional paths, e.g., "/static/" before adding to base64Array.
                  const cleanBase64Data = base64Data.replace(
                    /^data:image\/\w+;base64,/,
                    ""
                  );
                  base64Array.push(cleanBase64Data);
                }
                completed++;
  
                if (completed === imageLinks.length) {
                  callback(base64Array);
                }
              });
            }
          }
  
          const imageLinks = ["/static/3.png", "/static/1.png", "/static/2.png"];
  
          convertImagesToBase64(imageLinks, (base64Array) => {
            document.querySelector(
              "#imga"
            ).src = `data:image/png;base64,${base64Array[0]}`;
  
            imageCount = base64Array;
          });
  
          function changeGradient() {
            element.classList.remove(`gradient${currentGradient}`);
            document.body.classList.remove(`gradient${currentGradient}`);
  
            currentGradient = (currentGradient % 3) + 1;
            element.classList.add(`gradient${currentGradient}`);
            document.body.classList.add(`gradient${currentGradient}`);
  
            document.querySelector("#imga").style.opacity = "0";
  
            setTimeout(() => {
              document.querySelector("#imga").src = `data:image/png;base64,${
                base64Array[count - 1]
              }`;
  
              document.querySelector("#imga").style.opacity = "1";
  
              if (count === 1) {
                count = 3;
              } else {
                count = count - 1;
              }
            }, 300);
          }
  
          setInterval(changeGradient, 8000);
        });
        window.onscroll = function () {
          scrollFunction();
        };
        function per(element,c) {
    const style = window.getComputedStyle(element);
    const width = style.getPropertyValue('width');
    const numericValue = parseFloat(width.replace(/[^0-9.-]+/g, ""));
  
  if (c === 1){
      return numericValue
  }
    const result = numericValue - ((2 / 100) * numericValue);
  
    return result;
  }
        function scrollFunction() {
          if (
            document.body.scrollTop > 2 ||
            document.documentElement.scrollTop > 2
          ) {
              if (document.querySelector("#Sidenav.opend") ){
              document.querySelector(".tabular_parent").style.width = per(document.querySelector("nav"),1)+'px'}
              else{
                  document.querySelector(".tabular_parent").style.width = per(document.querySelector("nav"),1)+'px';
              }
            document.querySelector(".tabular_parent").style.right = "0%";
            document.querySelector(".tabular_parent").style.borderRadius = "0%";
            document.querySelector("nav").classList.add("scrolled");
          
          } else {
              if (document.querySelector("#Sidenav.opend") ){
              document.querySelector(".tabular_parent").style.width =per(document.querySelector("nav"),9)+'px'}
              else{
                  document.querySelector(".tabular_parent").style.width = per(document.querySelector("nav"),9)+'px';
              }
            document.querySelector(".tabular_parent").style.right = "1%";
            document.querySelector(".tabular_parent").style.borderRadius =
              "30px 30px 00 0";
            document.querySelector("nav").classList.remove("scrolled");
  
          }
        }
        function handleBreakpoints() {
          function okay() {
            const screenWidth = window.innerWidth;
  
            if (screenWidth <= 880) {
              const secElement = document.querySelector(".sec");
              secElement.style.display = "grid";
              secElement.style.opacity = 1;
              secElement.style.height = "auto";
  
              const firstElement = document.querySelector(".first");
              firstElement.style.display = "none";
              firstElement.style.opacity = 0;
              firstElement.style.height = 0;
            } else {
              const firstElement = document.querySelector(".first");
              firstElement.style.display = "grid";
              firstElement.style.opacity = 1;
              firstElement.style.height = "auto";
  
              const secElement = document.querySelector(".sec");
              secElement.style.display = "none";
              secElement.style.opacity = 0;
              secElement.style.height = 0;
            }
          }
          if (!document.startViewTransition) {
            okay();
            return;
          }
  
          // With View Transitions:
          document.startViewTransition(() => okay());
        }
  
        window.addEventListener("resize", handleBreakpoints);
        handleBreakpoints();

        function calculateTextWidth(text, fontSize, padding) {
          const tempElement = document.createElement('span');
          tempElement.style.position = 'absolute';
          tempElement.style.whiteSpace = 'nowrap';
          tempElement.style.visibility = 'hidden';
          tempElement.style.font = `${fontSize}px Arial, sans-serif`;
          tempElement.textContent = text;
        
          document.body.appendChild(tempElement);
        
          const textWidth = tempElement.offsetWidth;
        
          document.body.removeChild(tempElement);
        
          const totalWidth = textWidth + (2 * padding) + 5;
        
          const limitedWidth = totalWidth > 127 ? '127x' : `${totalWidth}px`;
        
          return limitedWidth;
        }

        const nameElement = document.querySelector('name');
        const textWidth = calculateTextWidth(nameElement.innerHTML, 15, 1);
        nameElement.style.width = textWidth;   