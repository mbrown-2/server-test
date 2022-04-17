function simple_get() {
    let meterID = document.getElementById("name").value;
    let theURL='/data/' + meterID;
    console.log("making a RESTful request to the server!");

    alert("pressed button");

    fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
            console.log(response['available'])


        }
    );
}