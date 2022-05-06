"use strict";

const key = "AIzaSyC4-YcTHOk8oj5wY_bQ4JxF2nxNZP1iOR0";
const script = document.createElement('script')
script.src = `https://maps.googleapis.com/maps/api/js?key=${key}&callback=initMap&libraries=visualization&v=weekly`
script.defer = ""

const script2 = document.createElement('script')
script2.src = "https://polyfill.io/v3/polyfill.min.js?features=default"
document.getElementsByTagName("head")[0].appendChild(script2)
document.getElementsByTagName("head")[0].appendChild(script)

function initMap() {

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: {
            lat: 39.952599,
            lng: -75.181780
        },
        mapTypeId: "terrain"
    });

    const request = new XMLHttpRequest();
    request.open('GET', '/api/locations');
    request.send();

    const locationCircleArray = []

    request.onload = () => {
        let locations = JSON.parse(request.responseText)
        for (const location in locations) {
            const locationCircle = new google.maps.Circle({
                strokeColor: locations[location].color,
                strokeOpacity: 1,
                strokeWeight: 2,
                fillColor: locations[location].color,
                fillOpacity: 0.7,
                map,
                center: locations[location]['center'],
                radius: 100
            });
            locationCircleArray.push(locationCircle);
        }
    }

    $("#selectUser").on('change', (e) => {
        const selectedOptionValue =  $(e.target).val()
        const selectedUser = parseInt(selectedOptionValue.slice(5, selectedOptionValue.length))
        
        const request = new XMLHttpRequest();
        request.open('GET', `/api/locations/user/${selectedUser}`);
        request.send();
        
        // remove previous circles
        locationCircleArray.forEach(singleLocationCircle => {
            singleLocationCircle.setMap(null);
        })

        request.onload = () => {
            let locations = JSON.parse(request.responseText)

            for (const location in locations) {
                const locationCircle = new google.maps.Circle({
                    strokeColor: locations[location].color,
                    strokeOpacity: 1,
                    strokeWeight: 2,
                    fillColor: locations[location].color,
                    fillOpacity: 0.7,
                    map,
                    center: locations[location]['center'],
                    radius: 100
                });
                locationCircleArray.push(locationCircle);
            }
        }

    })
    
}