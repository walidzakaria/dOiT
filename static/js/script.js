$(document).ready(function() {

    GetGeoLocation();

    CreateActivityTypeAutocomplete();


    //$("#id_lat").prop('disabled', true);
    //$("#id_lon").prop('disabled', true);

    $('#id_activity').on('focus', function(e) {
        CreateActivityAutocomplete();
    })

    $('#id_location').on('focusout', function() {
        let location = $('#id_location').val();
        if (location) {
            GetSearchedLocation(location);
        }
    })

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $('.dropdown-menu').find('form').click(function(e) {
        e.stopPropagation();
    });

    $('#select-country').on('input', function(e) {
        let search = $('#select-country').val();
        GetSuggestions(search, "select-country");
    });

    $('#activity-location').on('input', function(e) {
        let search = $('#activity-location').val();
        GetSuggestions(search, "activity-location");
    });

    $('#id_location').on('input', function(e) {
        let search = $('#id_location').val();
        GetSuggestions(search, "id_location");
    });

    $('#location-form').submit(function(e) {
        let searchText;
        searchText = $('#select-country').val();
        GetSearchedLocation(searchText);
        $('#location-form').removeClass('show');
        $('#location-list').removeClass('show');
        e.preventDefault();
    });


    ApplyStarRating();


    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);

    });

    $(".custom-file-input-with-pic").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        ReadURL(this);
    });

    function ReadURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                $('#profile-pic').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }


    $('#add-new-activity').submit(function(e) {
        e.preventDefault();
        AddNewActivityType(csrftoken);
    });


});

function CreateActivityTypeAutocomplete() {

    $.ajax({
        type: 'GET',
        url: '/activity-type-autocomplete/',
        dataType: 'json',
        data: {},
        success: function(data) {
            console.log(data.results);
            let activityTypeList = [];
            for (activityType of data.results) {
                activityTypeList.push(activityType.text);
                var activityTypeInput = document.getElementById("id_activity_type");
                if (activityTypeInput) {
                    InputAutocomplete(document.getElementById("id_activity_type"), activityTypeList);
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function CreateActivityAutocomplete() {
    let urlLink = '/activity-autocomplete/'
    let activityType = $('#id_activity_type').val();
    if (activityType) {
        urlLink = `${urlLink}?q=${activityType}`;
        urlLink = encodeURIComponent(urlLink.trim());
        console.log(urlLink);
    }
    $.ajax({
        type: 'GET',
        url: urlLink,
        dataType: 'json',
        data: {},
        success: function(data) {
            console.log(data.results);
            let activityList = [];
            for (activity of data.results) {
                activityList.push(activity.text);
                var activityInput = document.getElementById("id_activity");
                if (activityInput) {
                    InputAutocomplete(document.getElementById("id_activity"), activityList);
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

}

function AddNewActivityType(token) {
    let activityType = $('#activity-type').val();

    $.ajax({
        type: 'POST',
        url: '/api/activity-type/',
        dataType: 'json',
        data: {
            "activity_type": activityType
        },
        success: function(data) {
            $('h3').text('walid');
            console.log(data);
            AddNewActivity(data.activity_type_id, token);
        },
        error: function(error) {
            console.log(error);
        }
    });

}

function AddNewActivity(activityType, token) {
    let activity = $('#activity-name').val();
    $.ajax({
        type: 'POST',
        url: '/api/activity/',
        dataType: 'json',
        data: {
            "activity_type": activityType,
            "activity": activity
        },
        success: function(data) {
            console.log(data);
            AddUserActivity(data.activity_id, token);
            //AddNewActivity(response.activity_type_id, token);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function AddUserActivity(activity, token) {
    let location = $('#activity-location').val();
    let mon = $('#mon').prop("checked");
    let tue = $('#tue').prop("checked");
    let wed = $('#wed').prop("checked");
    let thu = $('#thu').prop("checked");
    let fri = $('#fri').prop("checked");
    let sat = $('#sat').prop("checked");
    let sun = $('#sun').prop("checked");
    let timeFrom = $('#time-from').val();
    let timeTo = $('#time-to').val();
    let description = $('#description').text();
    alert(description);
    alert(timeTo);
};

function ApplyStarRating() {
    $('.star-1').click(function() {
        $('.star').removeClass('checked');
        $('.rate-1').addClass('checked');
    });

    $('.star-2').click(function() {
        $('.star').removeClass('checked');
        $('.rate-1').addClass('checked');
        $('.rate-2').addClass('checked');
    });

    $('.star-3').click(function() {
        $('.star').removeClass('checked');
        $('.rate-1').addClass('checked');
        $('.rate-2').addClass('checked');
        $('.rate-3').addClass('checked');
    });

    $('.star-4').click(function() {
        $('.star').removeClass('checked');
        $('.rate-1').addClass('checked');
        $('.rate-2').addClass('checked');
        $('.rate-3').addClass('checked');
        $('.rate-4').addClass('checked');
    });

    $('.star-5').click(function() {
        $('.star').addClass('checked');
    });


}

function GetSearchedLocation(searchText) {
    searchText = encodeURIComponent(searchText.trim());
    let appId = '35mHfJ3nOmgsSR7Om5tn';
    let appCode = 'dXMLSO7UYuvI6U0Ns_OmRQ';

    let userLat;
    let userLong;
    let userLocation;

    let link = `https://geocoder.api.here.com/6.2/geocode.json?app_id=${appId}&app_code=${appCode}&searchtext=${searchText}`;

    $.ajax({
        type: 'GET',
        url: link,
        dataType: 'json',
        data: {},
        success: function(data) {
            console.log(data);
            let myData = data;
            userLocation = myData.Response.View[0].Result[0].Location.Address.Label;
            userLat = myData.Response.View[0].Result[0].Location.DisplayPosition.Latitude;
            userLong = myData.Response.View[0].Result[0].Location.DisplayPosition.Longitude;
            $('#locationLabel').text(userLocation);
            let locationList = userLocation.split(', ');
            $('#hidden-country').text(locationList[2]);
            $('#hidden-area').text(locationList[1]);
            $('#hidden-city').text(locationList[0]);
            $('#hidden-lat').text(userLat);
            $('#id_lat').val(userLat);
            $('#hidden-long').text(userLong);
            $('#id_lon').val(userLong);
            $('#location-form').removeClass('show');
            $('#location-list').removeClass('show');
        },
        error: function(error) {
            console.log(error);
        }
    });

};

function GetSuggestions(keywords, objectName, sticky) {
    keywords = keywords.replace(' ', '+');
    keywords = encodeURIComponent(keywords.trim());

    let appId = '35mHfJ3nOmgsSR7Om5tn';
    let appCode = 'dXMLSO7UYuvI6U0Ns_OmRQ';

    let link = `https://autocomplete.geocoder.api.here.com/6.2/suggest.json?app_id=${appId}&app_code=${appCode}&query=${keywords}&beginHighlight=<b>&endHighlight=</b>`
    $.ajax({
        type: 'GET',
        url: link,
        dataType: 'json',
        data: {},
        success: function(data) {

            //SuggestLocation(data.suggestions);
            ListAutoComplete(objectName, data.suggestions);

        },
        error: function(error) {
            console.log(error);
        }

    });

};

// general functions here!

function ListAutoComplete(objectName, suggestions) {
    function autocomplete(inp, arr) {
        /*the autocomplete function takes two arguments,
        the text field element and an array of possible autocompleted values:*/
        let currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function(e) {
            let a, b, i, val = this.value;
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

                    /*create a DIV element for each matching element:*/
                    b = document.createElement("DIV");
                    /*make the matching letters bold:*/
                    b.innerHTML = arr[i].label;

                    /*insert a input field that will hold the current array item's value:*/
                    let inputValue = arr[i].label.replace('<b>', '');
                    inputValue = inputValue.replace('</b>', '');
                    b.innerHTML += "<input type='hidden' value='" + inputValue + "'>";
                    /*execute a function when someone clicks on the item value (DIV element):*/
                    b.addEventListener("click", function(e) {
                        /*insert the value for the autocomplete text field:*/
                        let selectedText = this.getElementsByTagName("input")[0].value;
                        selectedText = selectedText.replace('<b>', '');
                        selectedText = selectedText.replace('</b>', '');
                        inp.value = selectedText;
                        /*close the list of autocompleted values,
                        (or any other open lists of autocompleted values:*/
                        closeAllLists();
                    });
                    a.appendChild(b);
                }

            }

        });
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            let x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
                /*If the arrow DOWN key is pressed,
                increase the currentFocus variable:*/

                currentFocus++;

                if (currentFocus >= x.length) currentFocus = 0;
                if (currentFocus < 0) currentFocus = (x.length - 1);

                /*and and make the current item more visible:*/
                //addActive(x);
                SetActive(x, currentFocus)
            } else if (e.keyCode == 38) { //up
                /*If the arrow UP key is pressed,
                decrease the currentFocus variable:*/
                currentFocus--;
                /*and and make the current item more visible:*/
                //addActive(x);

                if (currentFocus >= x.length) currentFocus = 0;
                if (currentFocus < 0) currentFocus = (x.length - 1);

                SetActive(x, currentFocus)
            } else if (e.keyCode == 13) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                if (currentFocus > -1) {
                    /*and simulate a click on the "active" item:*/
                    if (x) x[currentFocus].click();
                }
            }
        });

        function SetActive(x, activeIndex) {

            if (!isNaN(activeIndex)) {
                for (var i = 0; i < x.length; i++) {
                    x[i].classList.remove("autocomplete-active");
                }

                x[activeIndex].classList.add("autocomplete-active");
            };
        };
        //function addActive(x) {
        //    /*a function to classify an item as "active":*/
        //    if (!x) return false;
        //    /*start by removing the "active" class on all items:*/
        //    removeActive(x);
        //    if (currentFocus >= x.length) currentFocus = 0;
        //    if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/

        //    x[currentFocus].classList.add("autocomplete-active");

        //}

        //function removeActive(x) {
        //    /*a function to remove the "active" class from all autocomplete items:*/
        //    for (var i = 0; i < x.length; i++) {
        //        x[i].classList.remove("autocomplete-active");
        //    }
        // }

        function closeAllLists(elmnt) {
            /*close all autocomplete lists in the document,
            except the one passed as an argument:*/
            let x = document.getElementsByClassName("autocomplete-items");
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
        let userLocation;

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
                let myData = data;
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

    $.ajax({
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

function Wait(visibility, parent) {
    if (visibility) {
        $(parent).append(' <div class="spinner-border spinner-border-sm text-dark"></div>');

    } else {
        $('.spinner-border').remove();
    }
};


function InputAutocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
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