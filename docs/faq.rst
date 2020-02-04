Frequently asked questions
==========================

How do I copy data from the production database to the development database?
****************************************************************************

TODO

All my selenium tests keep failing
***********************************

Try to update FireFox and the geckodriver.

The website is not working. What should i do?
*********************************************

First you should check if the database is still running. You can check the status at https://dbod.web.cern.ch/.
If you see any problems to you should contact the service desk by creating a ticket.

If the problem is not related to the database then you should check your emails.
If you have setup your email address correctly then you should you have received an error traceback.

To prevents errors from happening you should never commit untested code to the master branch.
Untested code should only be pushed to the develop branch.

I cannot start the server with the development database:
********************************************************

Access to the development database is only possible within CERN GPN. So make sure that
you have access to the CERN network.
Also make sure that you have not accidentally activated a VPN or Proxy to another network.
