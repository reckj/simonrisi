<h1>Code Logic</h1>
<h2>General</h2>
<h3>Libraries</h3>
Code is written in Python 3.7.3 and uses the following libraries:
<ul>
<li>sys</li>
<li>time</li>
<li>pygame</li>
<li>RPi.GPIO</li>
</ul>
Libraries can be installed with the following command:

```
sudo pip3 install libraryname
```
Be sure that python is installed. If not, install it with:

``` 
sudo apt-get install python3
```
<h3>System</h3>
The program is designed to run on a Raspberry Pi with Raspbian. It uses the GPIO pins to read the signals from the gates. If the program is tested on a different system, the GPIO library must be commented out and debugMode must be set to <strong>True</strong>.
<h2>Debug Mode</h2>
If the <strong>debugMode</strong> variable is set to True, the program will use keys <strong>1 & 2</strong> as the triggers for the gates. This is useful for testing the program without the need for the gates and a raspberry. Additionally the program will generate terminal output for debugging purposes and will open the application window in a smaller size instead of fullscreen.
<h2>Variables</h2>
Set the following Variables in the main.py file:

```
debugMode = False
debounceDelay = 0.01 #delay in seconds
measurementDelay = 1 #delay in seconds
measurementTimeout = 4 #timeout in seconds
gateDistance = 1 #distance between the gates in meters

gate1Pin = 40
gate2Pin = 38
```

<h2>Classes</h2>
<h3>Timer</h3>
Class for measuring time. Can be started, stopped and reset. The time can be read in seconds though the <strong>getTime</strong> function.
<h3>SpeedGate</h3>
Main class for the gates. The following functions are available:
<ul>
<li><strong>update</strong>: updates the object: checks the gates & starts new measurement if measurementDelay elapsed</li>
<li><strong>changeState</strong>: changes state of SpeedGate object (not used in this iteratio)</li>
<li><strong>getSpeed</strong>: get the current speed</li>
<li><strong>checkGate</strong>: check if the gates are triggered</li>
<li><strong>calculateSpeed</strong>: calculates the current speed and sets previous speed</li>
<li><strong>measure</strong>: does a speed measurement with an integrated measurement timeout</li>
</ul>


<h2>Functions</h2>
<h3>setup</h3>
sets up pin mode and initializes the gates
<h3>readPin</h3>
reads the raw pin or keyboard input corresponding to the gate
<h3>debounceRead</h3>
does a debounce read of the gate
<h3>draw</h3>
updates the pygame window and renders the speed
<h3>main</h3>
main function of the program. Initializes the gates and starts the main loop






<h1>Instructions for autostart on Raspberry Pi w/ Raspbian</h1>
<h2>1. Make your script executable.</h2>

Open the terminal and navigate to the directory containing your script, then execute:

```
chmod +x main.py
```

<h2>2. Add to LXDE autostart.</h2>

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
@/path/to/your/python3 /path/to/your/script/main.py
```

Save and close the file. If you used nano, you can save by pressing CTRL + O, hit Enter, and then exit with CTRL + X.

<h2>3. Restart your Raspberry Pi.</h2>

Restart the Pi with:

```
sudo reboot
```

After rebooting, your script should automatically start running once the GUI is initialized. Ensure that any paths or resources your script relies on are absolute paths to prevent any potential issues during autostart.




<h1>Hardware</h1>
<h2>Parts</h2>
<ul>
<li>1x Raspberry Pi 4 Model B+</li>
<li>1x 16GB Micro SD Card</li>
<li>1x 12V Meanwell Power Supply</li>
<li>2x Pepperl+Fuchs RLK31-6/25/31/115 Reflexionslichtschranke</li>
<li>2x Refector</li>
<li>1x Housing Reflector</li>
<li>1x Housing Gate</li>
<li>2x 3D Printed Mounts for Relfectorgates</li>
</ul>
<h2>Electronics</h2>
<h3>Wiring</h3>
<h4>Reflector Gate</h4>
Connect the gate in a normally open configuration to the raspberry pi. The gate is triggered when the signal is pulled to ground - the pins are pulled high through the internal pullup resistor defined in the code. The pins can be defined in the main.py file. (default: 38 & 40)
<p>
<ul>
<li>White = Ground (Raspberry PI)</li>
<li>Black = Input Pin (Raspberry PI)</li>
<li>Grey = Not Connected</li>
<li>Brown = +12V (Power Supply)</li>
<li>Grey = Ground (Power Supply)</li>
</ul>
<p><em>important! use the board pin number to define pins and not their gpio number.</em>

The following diagram shows the wiring for the gate:

![Alt wiring](/speed/Documentation/GateDiagram.jpg "Gate Wiring")
