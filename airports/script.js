var flights;
var airports;

d3.csv("data/FOIA 2023-06030 (Elliott).csv").then(function (data) {
    window.flights = data;

    d3.csv("data/airports.csv").then(function (data) {
        window.airports = data;

        flights.forEach((flight) => {
            var match_arrival = airports.find((airport) => {
                return (
                    flight.arrival_airport === airport.faa ||
                    flight.arrival_airport === airport.icao
                );
            });
            var match_departure = airports.find((airport) => {
                return (
                    flight.departure_airport === airport.faa ||
                    flight.departure_airport === airport.icao
                );
            });
            var attributes = ["airport", "city", "country", "lat", "lng"];

            attributes.forEach(attribute=>{
                flight[`merge_departure_${attribute}`] = typeof match_departure !== 'undefined' ? match_departure[attribute] : "[UNKNOWN]";
                flight[`merge_arrival_${attribute}`] = typeof match_arrival !== 'undefined' ? match_arrival[attribute] : "[UNKNOWN]";
            })
        });

        flights.forEach(flight=>{
            var split = flight.date.split('-');
            flight.DateTime = `${split[0]}/${split[1]}/${split[2]} ${flight.departure_time}.00`
        })

        console.log(flights);
    });
});
