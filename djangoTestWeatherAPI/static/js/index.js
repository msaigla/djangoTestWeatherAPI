var username = ""

function changeCountry(value) {
    $("#citySelect2").val(null).trigger('change');
    $("#citySelect2").empty();
    if ($(value).val()) {
        $.ajax({
            data: {text: $(value).val()}, // получаем данные формы
            type: 'GET', // GET или POST
            url: "/get_cities/",
            // если успешно, то
            success: function (response) {
                let selected = "";
                for (let i = 0; i < (response.cities).length; i++) {
                    if (response.cities[i].name === "Moscow") {
                        selected = "selected";
                    } else {
                        selected = "";
                    }
                    $("#citySelect2")
                        .append(
                            "<option value='" + response.cities[i].id + "' " + selected + ">"
                            + response.cities[i].name +
                            "</option>"
                        ).trigger('change');
                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
        return false;
    }
}

function changeCity(value) {
    if ($(value).val()) {
        $("#findWeatherButton").prop("disabled", false);
    } else {
        $("#findWeatherButton").prop("disabled", true);
    }
    return false;
}


$("#findWeatherButton").click(function () {
    $.ajax({
        data: {
            id: $("#citySelect2").val(),
            country: $("#countrySelect2").val(),
        }, // получаем данные формы
        type: 'GET', // GET или POST
        url: "/get_weather/",
        // если успешно, то
        success: function (response) {
            $("#textWeather").html(response.weather);
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            alert(response.responseJSON.errors);
            console.log(response.responseJSON.errors);
        }
    });
    historyUserWeather();
    countSearchCity();
})

function countSearchCity() {
    console.log(username)
    $('#countSearchCity').html('');
    $.ajax({
        data: {}, // получаем данные формы
        type: 'GET', // GET или POST
        url: "/count_search_city/",
        // если успешно, то
        success: function (response) {
            console.log(response)
            for (let i = 0; i < (response.cities).length; i++) {
                $('#countSearchCity').append(
                    '<tr>\
                        <td>' + response.cities[i].country + '</td>\
                            <td>' + response.cities[i].name + '</td>\
                            <td>' + response.cities[i].count + '</td>\
                         </tr>'
                )
            }
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            alert(response.responseJSON.errors);
            console.log(response.responseJSON.errors);
        }
    });
}

countSearchCity()

function historyUserWeather() {
    console.log(username)
    $('#historiesUser').html('');
    if (username !== "") {
        $.ajax({
            data: {
                username: username,
            }, // получаем данные формы
            type: 'GET', // GET или POST
            url: "/get_history_user_weather/",
            // если успешно, то
            success: function (response) {
                for (let i = 0; i < (response.histories).length; i++) {
                    $('#historiesUser').append(
                        '<tr>\
                            <td>' + response.histories[i].country + '</td>\
                            <td>' + response.histories[i].name + '</td>\
                         </tr>'
                    )
                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    }
}