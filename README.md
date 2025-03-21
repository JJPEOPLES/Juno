Installation Guide for Juno
1. Clone the Repository
First, clone this repository to your local machine.

2. Setting up Juno
After cloning, copy the juno.bat file to a folder of your choice and add it to the system PATH:

Open Environment Variables in your system settings.
Create a new System variable called JUNO.
Paste the path to juno.bat (not juno2.bat, as it is currently bugged).
3. Running Your First Program
Navigate to the examples folder.
Run the following command to execute a Juno file:
bash
Copy
Edit
juno thank_you.juno
This is a small token of thanks for downloading the software!

Installation via install_juno.bat
Run install_juno.bat to automatically set up Juno and create a virtual environment if you want.

If you want to try the GUI, be aware that it’s currently bugged. I’d appreciate any help fixing it as I’m an indie dev. To install the GUI, use the following command:

bash
Copy
Edit
smh: jpm install gui
Contributing & Open Source
This software is open-source. Feel free to fork and make modifications as you wish. However, I do not accept people who simply copy the language without adding any value. If you're going to copy it, at least bring something useful to the table. We want innovation, not imitation!

Notes
Important: juno2.bat is currently bugged, so do not use it.
Please report any issues with the GUI or other features!
