Developer's Diary
===============
Per-app info and decisions.

``summary``
###########

- Instead of the ``terminaltables`` module, the ``prettytable`` one was preferred,
  because the former depended on the size of the terminal to resize the tables created,
  meaning that it depended on the size of the OpenShift terminal, which required a lot of ugly
  tweaks. ``prettytable`` is much cleaner.


