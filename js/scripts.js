/*!
* Start Bootstrap - Agency v7.0.5 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

window.addEventListener('DOMContentLoaded', event => {

    // home Navbar shrink function
    var homenavbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#homeNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    homenavbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', homenavbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const homeNav = document.body.querySelector('#homeNav');
    if (homeNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#homeNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropdownClick() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

// Alert for the release date of audition materials
// window.addEventListener('DOMContentLoaded', () => {
   
// })

window.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes("concerts")) {
        console.log(window.location.pathname);
        // Get the modal
        var modal = document.getElementById("posterModal");

        // Get the image and insert it inside the modal - use its "alt" text as a caption
        var fallImg = document.getElementById("fallImg");
        var springImg = document.getElementById("springImg");
        var modalImg = document.getElementById("modalImg");
        var captionText = document.getElementById("caption");
        fallImg.onclick = function(){
            modal.style.display = "block";
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        }
        springImg.onclick = function(){
            modal.style.display = "block";
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        }

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }

        // get the roster data
        fetchData();
    }
    
})

// getting roster data from flask api
function fetchData() {
    /***** switch between the file paths to either call the api or read from json ******/
    // api: 'http://127.0.0.1:5000/api/parsecsv'
    // json file: '../backend/api/roster.json'
    fetch('../backend/api/roster.json')
        .then(response => response.json())
        .then(data => {
            // document.getElementById('result').innerHTML = data.clarinet;
            addRoster(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function addRoster(data) {
    const instrumentSections = ['violin-1', 'violin-2', 'viola', 
                                'cello', 'flute', 'piccolo', 'oboe', 'clarinet',
                                'bassoon', 'horn','trumpet','trombone', 'tuba', 'percussion'];
    for (instrument of instrumentSections) {
        // define the key to access the data json
        key = instrument;
        // instrument is for defining instrumentContainer for HTML
        if (instrument == 'violin-1') {
            key = 'violin 1';
        } else if (instrument == 'violin-2') {
            key = 'violin 2';
        }
        // get players from each section and add them to HTML
        for (player of data[key]) {
            const instrumentContainer = document.getElementsByClassName(instrument)[0]
            const newName = document.createElement("span");
            newName.innerHTML = `${player} <br>`;
            instrumentContainer.appendChild(newName);
        }
    }
        

    
    
}
