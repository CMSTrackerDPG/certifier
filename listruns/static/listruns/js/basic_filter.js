$(document).ready(function () {
    const request_get_params= window.location.search.substr(1);

    if(request_get_params.indexOf("dataset") != -1 ||
        request_get_params.indexOf("dataset") != -1)
        $("#more").collapse('show');

    if(request_get_params.indexOf("date_range") != -1){
        $('#date_day').css('display', 'none');
        $('#date_range').css('display', 'inline');
    }

    $("#show-filter-btn").click(function () {
        $("#more").collapse('toggle');
    });

    $("#clear-filters").click(function () {
        $('#id_date_range_0').val("");
        $('#id_date_range_1').val("");
        $('#id_date_day').val(0);
        $('#id_date_month').val(0);
        $('#id_date_year').val(0);
        $('#id_type').val("");
        $('#id_dataset').val("");
        $('#id_runs_0').val("");
        $('#id_runs_1').val("");
        $('#id_pixel_problems').val("default").selectpicker("refresh");
        $('#id_strip_problems').val("default").selectpicker("refresh");
        $('#id_tracking_problems').val("default").selectpicker("refresh");
    });

    $("#radio_day").change(function () {
        $('#date_day').css('display', 'inline');
        $('#date_range').css('display', 'none');

        $('#id_date_range_0').val("");
        $('#id_date_range_1').val("");
    });


    $("#radio_range").change(function () {
        $('#date_day').css('display', 'none');
        $('#date_range').css('display', 'inline');

        document.getElementById("id_date_day").value = 0;
        document.getElementById("id_date_month").value = 0;
        document.getElementById("id_date_year").value = 0;
    });

    $("#more").on('show.bs.collapse', function () {
        $("#show-filter-btn").html('Show Less');
        $("#filter-button-top").css('display', 'none');
    });
    $("#more").on('hide.bs.collapse', function () {
        $("#show-filter-btn").html('Show More');
        $("#filter-button-top").css('display', 'inline');
    });
});
