Administration manual
=====================

The administrator has the most power in the website. He can create new
(local) users and is responsible for maintaining the website. He can
update or create the OAuth2 keys, which are necessary for CERN Single
sign-on.

The admin panel of the administrator consists of all of the same rights
that a shift leader has plus additional settings that for site
management.

.. note::
   
   You must be an Administrator in order to follow the procedures listed here

Roles
-----
To assign the Shifter or Shift Leader role to a user, follow the steps below:

#. Make sure that the user has already signed in using the **Login with CERN** button.
#. Navigate to the users administration page
     .. image:: images/admin-link.png   
#. Click on the **Users** link
     .. image:: images/admin-users.png
#. Search for the user you want to assign the role to and click on their username:
     .. image:: images/admin-user-to-assign.png
#. Under **User privilege**, select the appropriate role:
     .. image:: images/admin-change-role-shifter.png
#. Click on **SAVE**
	  
	   	   
Adding/Tweaking Checklist items
-------------------------------
Checklists appear on the `/update/` url of the app, and their purpose is to help
the Shifter keep track of the required checks that must be done before submission.

These can be configured from the admin panel.

**Checklists** are composed of **Checklist Groups**. Checklist Groups, are composed
of **Checklist Items**. So, if you need to add items to a specific Checklist, create
new Checklist Items and select the appropriate Checklist Group they should belong
to. 

An example of a checklist structure:

.. graphviz::
   
   digraph checklists {
   "Checklist Item" [color = green, shape = square, fixedsize=true, width=1.5]
   "Checklist Group" [color = blue, shape = square, fixedsize=true, width=1.5]
   "Checklist" [color = red, shape = square, fixedsize=true, width=1.5]

   "Checklist Item" -> "Checklist Group" [style=invis]
   "Checklist Group" -> "Checklist" [style=invis]   
   
   "Tracking" [color = red]
   "Bad components" [color = blue]
   "Tracking checks" [color = blue]
   "Check TkMaps" [color = green]
   "did we recover some 'known' bad component?" [color = green]
   "If yes, what is the reason to be flagged as bad?" [color = green]
   
   "did we recover some 'known' bad component?" -> "Bad components"
   "If yes, what is the reason to be flagged as bad?" -> "Bad components"   
   "Check TkMaps" -> "Tracking checks"
   "Bad components" -> "Tracking"
   "Tracking checks" -> "Tracking"
   }

   
