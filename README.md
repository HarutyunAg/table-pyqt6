# blackbox-pyqt6-table

Are you building a PyQT6 App and looking for an editable blackbox-ready2use editable table?  

*(づ◡﹏◡)づ Congrats!*  
You have found this repo.

This is a PyQt6 App featuring a fully editable table widget with essential functionalities right out of the box.

## project tree

```bash
blackbox/                # Main source directory
│
├── run.py               # Entrypoint for booting the application  
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

python .\blackbox\run.py
```
