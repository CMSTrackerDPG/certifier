function colorize_components(){
    $(".pixel, .sistrip, .tracking").each(function () {
        const component = $(this).html();
        if(component === "Good" || component === "Lowstat"){
            $(this).addClass("good-component")
        } else if (component === "Bad" || component === "Excluded"){
            $(this).addClass("bad-component")
        }
    })
}