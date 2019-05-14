$(document).ready(function () {

    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip();
    });

    $("#id-cc-input").keyup(function () {
        let text = $("#id-cc-input").val();

        $.ajax({
            url: '/ajax/validate-cc-list/',
            data: {
                'text': text
            },
            dataType: 'json',
            success: function (data) {
                if (data) {
                    let collisions_text = "";
                    $.each( data.collisions.good, function( key, value ) {
                        if(collisions_text !== "")
                            collisions_text += ", ";
                        collisions_text += '<span class="good-runs">' + value + '</span>'
                    });
                    $.each( data.collisions.bad, function( key, value ) {
                        if(collisions_text !== "")
                            collisions_text += ", ";
                        collisions_text += '<span class="bad-runs">' + value + '</span>'
                    });
                    $.each( data.collisions.prompt_missing, function( key, value ) {
                        if(collisions_text !== "")
                            collisions_text += ", ";
                        collisions_text += '<span class="prompt-missing-runs">' +value + '</span>'
                    });
                    $.each( data.collisions.changed_good, function( key, value ) {
                        if(collisions_text !== "")
                            collisions_text += ", ";
                        collisions_text += '<span class="changed-good-runs">' +value + '</span>'
                    });
                    $.each( data.collisions.changed_bad, function( key, value ) {
                        if(collisions_text !== "")
                            collisions_text += ", ";
                        collisions_text += '<span class="changed-bad-runs">' +value + '</span>'
                    });

                    let cosmics_text = "";
                    $.each( data.cosmics.good, function( key, value ) {
                        if(cosmics_text !== "")
                            cosmics_text += ", ";
                        cosmics_text += '<span class="good-runs">' + value + '</span>'
                    });
                    $.each( data.cosmics.bad, function( key, value ) {
                        if(cosmics_text !== "")
                            cosmics_text += ", ";
                        cosmics_text += '<span class="bad-runs">' + value + '</span>'
                    });
                    $.each( data.cosmics.prompt_missing, function( key, value ) {
                        if(cosmics_text !== "")
                            cosmics_text += ", ";
                        cosmics_text += '<span class="prompt-missing-runs">' +value + '</span>'
                    });
                    $.each( data.cosmics.changed_good, function( key, value ) {
                        if(cosmics_text !== "")
                            cosmics_text += ", ";
                        cosmics_text += '<span class="changed-good-runs">' +value + '</span>'
                    });
                    $.each( data.cosmics.changed_bad, function( key, value ) {
                        if(cosmics_text !== "")
                            cosmics_text += ", ";
                        cosmics_text += '<span class="changed-bad-runs">' +value + '</span>'
                    });

                    let missing_text = "";
                    $.each( data.missing, function( key, value ) {
                        if(missing_text !== "")
                            missing_text += ", ";
                        missing_text += '<span class="missing-runs">' + value + '</span>'
                    });

                    let legend = "";
                    if(data.collisions.good.length > 0 || data.cosmics.good.length > 0)
                        legend += '<span class="good-runs">GOOD</span> ';
                    if(data.collisions.bad.length > 0 || data.cosmics.bad.length > 0)
                        legend += '<span class="bad-runs">BAD</span> ';
                    if(data.missing.length > 0)
                        legend += '<span class="missing-runs">MISSING</span> ';
                    if(data.collisions.prompt_missing.length > 0 || data.cosmics.prompt_missing.length > 0)
                        legend += '<span class="prompt-missing-runs">PROMPT MISSING</span> ';
                    if(data.collisions.changed_good.length > 0 || data.cosmics.changed_good.length > 0)
                        legend += '<span class="changed-good-runs"">CHANGED TO GOOD</span> ';
                    if(data.collisions.changed_bad.length > 0 || data.cosmics.changed_bad.length > 0)
                        legend += '<span class="changed-bad-runs">CHANGED TO BAD</span> ';

                    let newtext = "";
                    if(collisions_text)
                        newtext += "Collisions: " + collisions_text + "<br/>";
                    if(cosmics_text)
                        newtext += "Cosmics: " + cosmics_text + "<br/>";
                    if(missing_text)
                        newtext += "Missing: " + missing_text + "<br/>";

                    $("#id-cc-span").html("<br/>" + newtext);
                    $("#id-cc-legend").html("<br/>Legend:" + legend);
                }
            }
        });
    });
});
