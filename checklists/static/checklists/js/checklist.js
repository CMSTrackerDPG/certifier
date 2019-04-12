/************************
 * CHECKLIST
 *
 * checklists helper functions
 ************************/

/**
 * Pops up the checklist modal when trying to check the checkbox.
 * All checklist items in the modal have to be checked in order to
 * set the main checklist checkbox (e.g. Pixel Checklist)
 */
function popupChecklistModal(checkbox){
    if (checkbox.attr("id").indexOf("item_") === -1) // only on main checkbox
    {
        checkbox.click(function () {
            const checklist = checkbox.attr("id").replace("id_checklist_","");
            $("#modal-"+checklist+"-id").modal();
            return false;
        });
    }
}

/**
 * @param checklist_id: e.g. sistrip
 *
 * Checks if all checklist items have been ticked via html
 * and sets the main checklist checkbox e.g. [x] Pixel Checklist
 *
 * Will be called when the "OK" button in a modal is clicked.
 * It does not submit the form, because it is only used to validate
 * that all checklist items have been ticked.
 */
function validateChecklist(checklist_id) {
    $("#modal-" + checklist_id + "-id").modal('hide');
    $("#id_checklist_" + checklist_id).prop('checked', true);
    return false; // Do not submit the modal form!
}

/**
 * Checks all items in the modal of the specified checklist
 * @param checklist_id: e.g. sistrip
 */
function checkAllItems(checklist_id) {
    $('[id^="id_checklist_"]').each(function() {

        if ($(this).attr("id").indexOf("item_") !== -1 && $(this).attr("id").indexOf(checklist_id) !== -1 ) {
            $(this).prop('checked', true);
        }
    });
}

function checkAllChecklists(){
    $("#id_checklist_general").prop("checked", true);
    $("#id_checklist_trackermap").prop("checked", true);
    $("#id_checklist_pixel").prop("checked", true);
    $("#id_checklist_sistrip").prop("checked", true);
    $("#id_checklist_tracking").prop("checked", true);
}

