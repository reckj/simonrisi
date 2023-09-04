<h1>Instructions for autostart on Raspberry Pi w/ Raspbian</h1>
Make your script executable.

Open the terminal and navigate to the directory containing your script, then execute:

```
chmod +x my_script.py
Add to LXDE autostart.
```
Open the autostart file in a text editor with:

```
nano ~/.config/lxsession/LXDE-pi/autostart
```

If the ~/.config/lxsession/LXDE-pi/ directory doesn't exist, you may need to create it.

```
mkdir -p ~/.config/lxsession/LXDE-pi/
```

And then create the autostart file:

```
touch ~/.config/lxsession/LXDE-pi/autostart
```

Once you're in the editor, add the following line at the end of the file:

```
@/path/to/your/python3 /path/to/your/my_script.py
```

Save and close the file. If you used nano, you can save by pressing CTRL + O, hit Enter, and then exit with CTRL + X.

Restart your Raspberry Pi.

Restart the Pi with:

```
sudo reboot
```

After rebooting, your script should automatically start running once the GUI is initialized. Ensure that any paths or resources your script relies on are absolute paths to prevent any potential issues during autostart.