$(document).ready(function() {


    GetGeoLocation();

    $('form').submit(function(e) {
        e.preventDefault();

    });

    $('.dropdown-menu').find('form').click(function(e) {
        e.stopPropagation();
    });

    $('#select-country').on('input', function(e) {
        let search = $('#select-country').val();
        GetSuggestions(search);
    });

    SuggestLocation();
});


function GetSuggestions(keywords) {
    keywords = keywords.replace(' ', '+');
    let link = `http://autocomplete.geocoder.api.here.com/6.2/suggest.json?app_id=35mHfJ3nOmgsSR7Om5tn&app_code=dXMLSO7UYuvI6U0Ns_OmRQ&query=${keywords}`
    $.ajax({
        type: 'GET',
        url: link,
        dataType: 'json',
        data: {},
        success: function(data) {

            //SuggestLocation(data.suggestions);
            ListAutoComplete("select-country", data.suggestions);

        },
        error: function(error) {
            console.log(error);
        }

    });

};

function SuggestLocation(data) {


};

// general functions here!

function ListAutoComplete(objectName, suggestions) {
    function autocomplete(inp, arr) {
        /*the autocomplete function takes two arguments,
        the text field element and an array of possible autocompleted values:*/
        var currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function(e) {
            var a, b, i, val = this.value;
            /*close any already open lists of autocompleted values*/
            closeAllLists();
            if (!val) {
                return false;
            }
            currentFocus = -1;
            /*create a DIV element that will contain the items (values):*/
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            this.parentNode.appendChild(a);
            /*for each item in the array...*/
            if (arr && arr.length > 0) {
                for (i = 0; i < arr.length; i++) {
                    /*check if the item starts with the same letters as the text field value:*/

                    if (arr[i].label.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = "<strong>" + arr[i].label.substr(0, val.length) + "</strong>";
                        b.innerHTML += arr[i].label.substr(val.length);
                        /*insert a input field that will hold the current array item's value:*/
                        b.innerHTML += "<input type='hidden' value='" + arr[i].label + "'>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function(e) {
                            /*insert the value for the autocomplete text field:*/
                            inp.value = this.getElementsByTagName("input")[0].value;
                            /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                        });
                        a.appendChild(b);
                    }
                }

            }

        });
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
                /*If the arrow DOWN key is pressed,
                increase the currentFocus variable:*/
                currentFocus++;
                /*and and make the current item more visible:*/
                addActive(x);
            } else if (e.keyCode == 38) { //up
                /*If the arrow UP key is pressed,
                decrease the currentFocus variable:*/
                currentFocus--;
                /*and and make the current item more visible:*/
                addActive(x);
            } else if (e.keyCode == 13) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                if (currentFocus > -1) {
                    /*and simulate a click on the "active" item:*/
                    if (x) x[currentFocus].click();
                }
            }
        });

        function addActive(x) {
            /*a function to classify an item as "active":*/
            if (!x) return false;
            /*start by removing the "active" class on all items:*/
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = (x.length - 1);
            /*add class "autocomplete-active":*/
            x[currentFocus].classList.add("autocomplete-active");
        }

        function removeActive(x) {
            /*a function to remove the "active" class from all autocomplete items:*/
            for (var i = 0; i < x.length; i++) {
                x[i].classList.remove("autocomplete-active");
            }
        }

        function closeAllLists(elmnt) {
            /*close all autocomplete lists in the document,
            except the one passed as an argument:*/
            var x = document.getElementsByClassName("autocomplete-items");
            for (var i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }
        /*execute a function when someone clicks in the document:*/
        document.addEventListener("click", function(e) {
            closeAllLists(e.target);
        });
    }

    /*An array containing all the country names in the world:*/
    //var countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antigua & Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia & Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central Arfrican Republic", "Chad", "Chile", "China", "Colombia", "Congo", "Cook Islands", "Costa Rica", "Cote D Ivoire", "Croatia", "Cuba", "Curacao", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Polynesia", "French West Indies", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauro", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saint Pierre & Miquelon", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "St Kitts & Nevis", "St Lucia", "St Vincent", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor L'Este", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks & Caicos", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Virgin Islands (US)", "Yemen", "Zambia", "Zimbabwe"];

    /*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
    autocomplete(document.getElementById(objectName), suggestions);




};

function GetGeoLocation() {

    geoLoc = navigator.geolocation.watchPosition(function(position) {
            navigator.geolocation.getCurrentPosition(ShowPosition);
            navigator.geolocation.clearWatch(geoLoc);
        },
        function(error) {
            if (error.code == error.PERMISSION_DENIED) {
                GetIp();
            }
        });


    function ShowPosition(position) {
        //let myHereKey = 'cFHqDkSD45dr2TDLBDaxWt4aPfsqcEbLed4LTz0bCyo';
        let appId = '35mHfJ3nOmgsSR7Om5tn';
        let appCode = 'dXMLSO7UYuvI6U0Ns_OmRQ';
        let userLat;
        let userLong;
        userLat = position.coords.latitude;
        userLong = position.coords.longitude;

        let apiLink = `https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox=${position.coords.latitude}%2C${position.coords.longitude}&mode=retrieveAreas&app_id=${appId}&app_code=${appCode}&gen=9`;
        let locationName = '';

        $.ajax({
            type: 'GET',
            url: apiLink,
            dataType: 'json',
            data: {},
            async: true,
            success: function(data) {
                console.log(data);
                var myData = data;
                userLocation = myData.Response.View[0].Result[0].Location.Address.Label;
                $('#locationLabel').text(userLocation);
                let locationList = userLocation.split(', ');
                $('#hidden-country').text(locationList[2]);
                $('#hidden-area').text(locationList[1]);
                $('#hidden-city').text(locationList[0]);
                $('#hidden-lat').text(userLat);
                $('#hidden-long').text(userLong);
            },
            error: function(error) {
                GetIp();
            }
        });

    };

};

function GetIp() {
    let ipAdress = '';

    var getIp = $.ajax({
        type: 'GET',
        url: 'https://jsonip.com?callback=?',
        dataType: 'json',
        data: {},
        success: function(data) {
            ipAddress = data.ip.split(',')[0];
            console.log(ipAddress);
            $('#hidden-ip').text(ipAddress);
            GetIpLocation(ipAddress);
            return ipAddress;
        },
        error: function(error) {
            console.log(error);
            return '';
        }
    });
};

function GetIpLocation(ipAddress) {
    let link = `https://extreme-ip-lookup.com/json/${ipAddress}`;

    $.ajax({
        type: 'GET',
        url: link,
        dataType: 'json',
        data: {},
        success: function(data) {
            //console.log(data);
            let country, region, city, lat, long;
            country = data.country;
            region = data.region;
            city = data.city;
            lat = data.lat;
            long = data.lon;

            $('#locationLabel').text(`${city}, ${region}, ${country}`);
            $('#hidden-country').text(country);
            $('#hidden-area').text(region);
            $('#hidden-city').text(city);
            $('#hidden-lat').text(lat);
            $('#hidden-long').text(long);
        },
        error: function(error) {
            console.log(error);
        }
    });

};