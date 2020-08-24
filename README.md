# PyQtMenu
A PyQt5 menu to display my apps or any .desktop file

<img src="https://raw.githubusercontent.com/Daguhh/PyQtMenu/master/Screenshot.png" width="600">

* Display desktop files into multiple tab, 
* Drag'n'Drop desktop file to add it in menu

new :
* Reduce mode : reduce launcher to a small floating button at application lauch

### Add a launcher
You should have a .desktop file with the following entries:
```
[Desktop Entry]
Name=My_App_Name
Comment=My App Description
Exec=My/app/path/my_app
Icon=My/icon/path/my_icon.png
```
Put it under 
```
Apps/your_catergory/my_app.desktop
```
or drag 'n' drop it to the wanted category tab

### Usage
Just run
```bash
./pyqtmenu
```
