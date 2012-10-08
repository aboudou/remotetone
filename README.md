RasPiRepCol
===========

RemoteTone (Beta) is a try to work with an Asus AI Remote from a (dead) Asus motherboard package and a Raspberry Pi, using Python programming language.
You can have more information into “doc” folder.

* [Youtube video](http://www.youtube.com/watch?v=kc6Tf4Gn1P8)

Remote management code cames from [ai-remote github project](https://github.com/Babar/ai-remote)

Requirements
------------

* First of all : a Raspberry Pi
* An Asus AI Remote and its IR receiver
* Python (with Debian / Raspbian : packages “python” and “python-dev”)
* RPi.GPIO library (0.4.0a or newer). On Raspbian, install package “python-rpi.gpio”.
* pyUSB library. On raspbian, install package “python-usb”.
* A small piezzo buzzer. Try to find a 3.3V one if you want the sound to be enough loud.
* A 330Ω resistor.

You have to connect : 
* One side of the resistor to pin #7 on the GPIO header
* The other side of the resistor to the “+” connector of the buzzer
* The other connector of the buzzer to the ground pin of the GPIO header (pin #6) 

How to use RemoteTone
---------------------

You'll first have to build the assembly, and plug it to the Raspberry Pi. Then plug the IR receiver to one of the USB connector of the Raspberry Pi. The receiver should be automatically detected. With a `lsusb` command, you should have the following line visible : `Bus 001 Device 004: ID 0b05:172e ASUSTek Computer, Inc.` (device number may differ).

You then have to start RemoteTone with `python remote_tone.py`, and change frequency with “+” and “-” buttons of the remote. In case of an USB timeout error on launch, you just have to start again RemoteTone.

When you want to stop the program, either hit `Ctrl + C` or press "Power" button of the remote.
