CertHelper internals
====================
Information regarding the internals of this Django project, mainly targeting developers.

``certifier``
#############

Views
*****

``certify``
___________
This complicated view contains multiple functionalities:

* Displays a form to certify a combination of run number & reconstruction type
* Allows the user to submit a complete certification form.
* Allows the user to display and add new :guilabel:`Bad Reasons`.


The user can land on this page from:

* The `/openruns/` page:
  
  * By selecting a run number and (optionally) a reconstruction type on the top form (``GET`` request).
  * By clicking a colored button in the results listed after searching for openruns (bottom form, ``GET`` request).
	
* The `/certify/` page:

  * By submitting the complete certification form (``POST`` Request)
  * By clicking on the :guilabel:`+` sign next to the :guilabel:`Bad Reasons` dropdown menu (``POST XMLHttpRequest``).


Bad Reasons
^^^^^^^^^^^
The form to submit a new bad reason is dynamically loaded via jQuery from the `/addbadreason/` URL and stored in the ``div`` with ``id="addBadReason"``. When the button to submit a new bad reason is pressed, a `POST XMLHttpRequest` is made to `/certify/` with the ``name`` and ``description`` of the new bad reason.


