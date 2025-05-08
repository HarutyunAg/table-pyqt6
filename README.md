# blackbox editable table for PyQT6

Are you building a PyQT6 App and looking for a blackbox / ready to use / eazy integratable / full editable table? I know u r.  

*(づ◡﹏◡)づ Congrats! You have found this repo.*  

This is not standalone app. It's just a table with bunch of regular  features. 

So speaking about features btw:
- edit values in cells
- drag and drop row
- save table
- upload table
- find values in table
- replace values in table

## shortcuts
You can change shortcuts in json file `blackbox/app/static/namespace/shortcuts.json`

```json
{
    "bar": {
        "file_menu": {
            "upload": "Ctrl+O",
            "save": "Ctrl+S"
        }
    },
    "table" : {
        "add_row_above" : "Ctrl+Up",
        "add_row_below": "Ctrl+Down",
        "remove_row": "Ctrl+Delete",
        "replace": "Ctrl+R",
        "find": "Ctrl+F"
    }
```

## project tree

```bash
blackbox/                # Main source directory
│
├── example.py           # File for representing example of usage  
│
├── app/                 # Core application logic and components  
    │
    ├── bar/             # Bar module for various application tools
    │
    ├── static/          # Static assets and dependencies  
    │   │
    │   ├── imgs/        # Directory for storing images, including logos and icons  
    │   │
    │   └── namespace/   # Namespace for labels, shortcuts, or other reusable elements  
    │
    └── table/           # Module for table-related features and views  
        │
        └── dialogs/     # Dialog components for user interactions and prompts  
```


### setup

```bash
git clone https://github.com/HarutyunAg/blackbox-pyqt6-table.git

cd blackbox-pyqt6-table

uv sync

uv run main.py
```

You can see example of usage this table widget in your *QMainWindow* in \blackbox\example.py

-----

When running a PyQt6/PySide2 application on Linux, you may encounter:
```
    Failed to create wl_display (No such file or directory)  
    qt.qpa.plugin: Could not load the Qt platform plugin "xcb" or "wayland"  
```
Solution:  
    Install the missing Qt Wayland package:  

```bash
sudo apt install qtwayland5
```

#TODO
- add gif to readme  
- add system sep to path str
