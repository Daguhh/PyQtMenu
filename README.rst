
|badge_MIT| |badge_python| |badge_download|

.. |badge_MIT| image:: https://img.shields.io/badge/License-MIT-blue.svg 
.. |badge_download| image:: https://img.shields.io/github/downloads/Naereen/StrapDown.js/total.svg 
.. |badge_python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg

********
PyQtMenu
********

A PyQt5 menu to display my apps or any .desktop file

* Display desktop files into multiple tab, 
* Drag'n'Drop desktop file to add it in menu

new :

* Reduce mode : reduce launcher to a small floating button at application lauch
* Dual panel view (with i3) : control windows positions from tab "layout"

        .. image:: https://raw.githubusercontent.com/Daguhh/PyQtMenu/reduce_mod/Screenshots/screens.gif
          :width: 200px
          :align: center
          :alt: PyQtMenu preview

Usage
#####

Just run::

  ./pyqtmenu.py


Add a launcher
###############

You should have a .desktop file with the following entries::

  [Desktop Entry]
  Name=My_App_Name
  Comment=My App Description
  Exec=My/app/path/my_app
  Icon=My/icon/path/my_icon.png

Put it under::

  ~/.config/pyqtmenu/Apps/your_catergory/my_app.desktop

or drag 'n' drop it to the wanted category tab

Configuration :
###############

Graphically
-----------

You can configure the menu by the interface (add icon, change icon size/theme)

when you're happy with your save it (Fichier > save)

Text file :
-----------

All configurations can be found in::

  ~/.config/pyqtmenu
  
============= ====================================  
file          description   
============= ====================================  
Apps/          category/my_app.desktop location  
------------- ------------------------------------
app_save.json cache file for .desktop   
------------- ------------------------------------
config.ini    User configuration file   
============= ====================================  
