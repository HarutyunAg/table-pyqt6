# blackbox-pyqt6-table

Are you building a PyQT6 App and looking for a blackbox-ready2use editable table?  

*(づ◡﹏◡)づ Congrats!*  
You have found this repo.

This is a PyQt6 fully editable table widget with essential functionalities right out of the box.

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

poetry install

poetry shell

python .\blackbox\example.py
```

You can see example of usage this table widget in your *QMainWindow* in \blackbox\example.py
