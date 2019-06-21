function disable_date_dropdown_lists() {
    // disables every date dropdown list
    // to simplify url get parameters

    $( "select[name^='date__lte_']" ).each(function(){
        $(this).attr("disabled", "disabled");
    });

    $( "select[name^='date__gte_']" ).each(function(){
        $(this).attr("disabled", "disabled");
    });
}

function simplify_date_filter_parameters(form){
    // converts:
    // ?date__gte_day=2&date__gte_month=7&date__gte_year=2018&date__lte_day=8&date__lte_month=7&date__lte_year=2018
    // to:
    // ?date__gte=2018-7-2&date__lte=2018-7-8

    const gte_day = $("select[name='date__gte_day']").val();
    const gte_month = $("select[name='date__gte_month']").val();
    const gte_year = $("select[name='date__gte_year']").val();

    const lte_day = $("select[name='date__lte_day']").val();
    const lte_month = $("select[name='date__lte_month']").val();
    const lte_year = $("select[name='date__lte_year']").val();

    disable_date_dropdown_lists();

    let date_gte;
    if (gte_day !== "0" && gte_day !== null && gte_day !== "") {
        date_gte = gte_year + "-" + gte_month + "-" + gte_day;
        $('<input />').attr('type', 'hidden')
            .attr('name', "date__gte")
            .attr('value', date_gte)
            .appendTo(form);
    }
    let date_lte;
    if (lte_day !== "0" && lte_day !== null && lte_day !== "") {
        date_lte = lte_year + "-" + lte_month + "-" + lte_day;
        $('<input />').attr('type', 'hidden')
            .attr('name', "date__lte")
            .attr('value', date_lte)
            .appendTo(form);
    }
}

function ignore_unwanted_filters(form){
    let checked_element = $(".ignore-other-filter-checkbox:checked");
    if(checked_element.length > 0){
        checked_element = checked_element.attr('id').replace('id-ignore-', '');
        form.find(":input").filter(function () {
            return !(this.id.indexOf(checked_element) !== -1);
        }).val("");
    }
}

function disable_empty_filter_fields(form){
    // disables every input field in a form
    // such that it does not appear as a
    // GET parameter in the url

    form.find(":input").filter(function () {
        return !this.value || this.value === "0";
    }).attr("disabled", "disabled");
}

/**
 * Offset the given date by the number of given days
 *
 * returns a Date object
 *
 * Example:
 * offset_date("2018-05-13", 2) -> "2018-05-15"
 * offset_date("2018-05-1", -3) -> "2018-04-28"
 */
function offset_date(date, day_offset){
    let new_date = new Date(date);
    new_date.setDate(date.getDate() + day_offset);
    return new_date
}

/**
 * Returns the weeks monday of a given date
 *
 * Example:
 * get_monday("2018-08-28") -> "2018-08-27"
 */
function get_monday(date) {
    let monday = new Date(date);

    // in Date() week begins with sunday
    const day = (date.getDay() - 1) % 7;  // make monday the start of week, not sunday

    monday.setDate(date.getDate() - day);
    return monday
}

/**
 * Returns the weeks sunday of a given date
 *
 * Example:
 * get_sunday("2018-08-28") -> "2018-09-02"
 */
function get_sunday(date) {
    let sunday = get_monday(date);
    sunday.setDate(sunday.getDate() + 6);
    return sunday
}

function set_date_range_filter_to_this_week(){
    const today = new Date(); // current date
    const monday = get_monday(today);
    const sunday = get_sunday(today);

    set_date_range_filter(monday, sunday);
}

function set_date_range_filter_to_last_week(){
    const today = new Date();
    const about_a_week_ago = offset_date(today, -7);

    const monday = get_monday(about_a_week_ago);
    const sunday = get_sunday(about_a_week_ago);

    set_date_range_filter(monday, sunday);
}

function set_week_to_previous(){
    const selected_date = get_set_filter_date_from();
    const about_a_week_ago = offset_date(selected_date, -7);

    const monday = get_monday(about_a_week_ago);
    const sunday = get_sunday(about_a_week_ago);

    set_date_range_filter(monday, sunday);
}

function set_week_to_next(){
    const selected_date = get_set_filter_date_to();
    const about_a_week_after = offset_date(selected_date, 6);

    const monday = get_monday(about_a_week_after);
    const sunday = get_sunday(about_a_week_after);

    set_date_range_filter(monday, sunday);
}

function set_date_range_filter_to_today(){
    const today = new Date();
    set_date_range_filter(today, today);
}

/**
 * @returns Date "from:" date that was set in the filter panel
 */
function get_set_filter_date_from(){
    const day = $("#id_date__gte_day").val();
    const month = $("#id_date__gte_month").val();
    const year = $("#id_date__gte_year").val()

    return new Date(year + "-" + month + "-" + day);
}

/**
 * @returns Date "to:" date that was set in the filter panel
 */
function get_set_filter_date_to(){
    const day = $("#id_date__lte_day").val();
    const month = $("#id_date__lte_month").val();
    const year = $("#id_date__lte_year").val();

    return new Date(year + "-" + month + "-" + day);
}

function set_date_range_filter(date_from, date_to){
    $("#id_date__gte_day").val(date_from.getDate());
    $("#id_date__gte_month").val(date_from.getMonth() + 1);
    $("#id_date__gte_year").val(date_from.getFullYear());

    $("#id_date__lte_day").val(date_to.getDate());
    $("#id_date__lte_month").val(date_to.getMonth() + 1);
    $("#id_date__lte_year").val(date_to.getFullYear());

    update_filter_week_display();
}

function uncheck_all_ignore_other_filter_checkboxes(){
    $(".ignore-other-filter-checkbox").each(function(){
        var checkbox = $(this);
        checkbox.prop("checked", false);
    });
}

/**
 * Source: https://weeknumber.net/how-to/javascript
 *
 * @returns {number} the ISO week of the date.
 */
Date.prototype.getWeek = function() {
  var date = new Date(this.getTime());
   date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  var week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                        - 3 + (week1.getDay() + 6) % 7) / 7);
};

function update_filter_week_display(){
    const date_from = get_set_filter_date_from();
    const date_to = get_set_filter_date_to();
    const week_from = date_from.getWeek();
    const week_to = date_to.getWeek();

    if(week_from === week_to){
        $("#id_filter_week_display").html("Week " + week_from);
    } else {
        $("#id_filter_week_display").html("");
    }
}

$("#id_date__gte_year, #id_date__gte_month, #id_date__gte_day, #id_date__lte_year, #id_date__lte_month, #id_date__lte_day").change(function () {
   update_filter_week_display();
});
update_filter_week_display(); // on page load
