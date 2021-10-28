# ZoomHelper v0.9.7

## What is it for?

This program is for joining meetings easily with one click without entering any password or id.

---
## Usage
The usage is simple just run the python file and it is done. Firstly you need to enter your meetings infos' into the program.

py zoomhelper.py

---
## Config (old info for v0.3)
You can access the GUI with -c or --config arguments.

py zoomhelper.py -c or py zoomhelper.py --config

![GUI.png](https://user-images.githubusercontent.com/72021576/136834720-d2964001-6228-4d82-af5c-c0d59a3aa8f0.png)

After running the command this ~~terrible~~ simple GUI greets you. You can add your meetings from here. It is pretty simple. You can only add meetings. You cannot delete meetings. So think twice before adding a meeting. (You can always delete it from JSON file.)

* **Name** is the name of the meeting. Can be empty.
* **ID** and **Password** are self-explanatory. They are needed.
* **Day** is 0 to 6. (0 means Monday and 6 means Sunday)
* **StartTime** is not necessary. The program only checks for **endTime**.
* Time format is 24H and only numbers. (exp. 1230)

---
# How does it work?
The way program works is firstly it compares the day if they are equal it checks the time and if real time is smaller than meeting time it will open the meeting.

---
## Future Plans
* Calendar like GUI ✔
* Delete meetings via GUI ✔
* Edit meetings via GUI ✔
* Good looking UI
* Conflicting meeting support ✔
* Add non-repetitive meetings ✔
* Support for other meeting apps
* Auto-open
