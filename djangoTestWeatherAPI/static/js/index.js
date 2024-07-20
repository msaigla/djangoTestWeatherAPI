function changeCountry(value) {
    $("#citySelect2").val(null).trigger('change');
    $("#citySelect2").empty();
    if ($(value).val()) {
        $.ajax({
            data: {text: $(value).val()}, // получаем данные формы
            type: 'GET', // GET или POST
            url: "http://127.0.0.1:8000/get_cities/",
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
        url: "http://127.0.0.1:8000/get_weather/",
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
})