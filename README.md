# Lucca 58HE
The Lucca 58HE is a 58 key hall effect split keyboard!

NEW STATUS UPDATE:

Left half of the keyboard is now perfectly functioning under KMK! changing the actuation from from 0 to 3.5mm is possible, but some weirdness means theres a deadzone towards the end of the keystroke, it can be fixed by increasing the distance between the switch plate and PCB so not a big deal. Could probably be avoided with different HE sensors?


OLD STATUS UPDATES:
Working with QMK has proved a lot more difficult than i thought, so im going to get it working with KMK and circuitpython first, and then worry about QMK support after!

Hall effect sensors are currently resulting in a resolution of 0.00706mm inanalog switch, so things are looking very promising :)My choice of HE sensor results in a voltage range of ~0 to ~0.4v, so using a different HE sensor with a greater sensitivity (not to be confused wit resolution) could result in even greater resolution of distance traveled, as the 12bit ADC on the RP2040 references the internal 3.3v. Am going on family holiday soon so progress will slow down a lot, may not be able to finish the project until the new year...

TO DO:
- Callibration for LHS [○]
- Callibration for RHS [○]
- Callibration output [ ]
- Auto Callibration [ ]
- Key actuation [ ]
- Per key varying actuation [ ]
- Rapid Trigger [ ]
- Communication between LHS & RHS [ ]
- LEDs [ ]
- OLEDs [ ]
- SPI communication between halves? [ ]

![IMG_6613](https://github.com/Maka8295/Lucca-58HE/assets/108311420/4b1c28fb-dfae-451a-887c-c89deb428f4d)


![IMG_6614](https://github.com/Maka8295/Lucca-58HE/assets/108311420/ee2d040d-f45c-473e-afe9-ba04d163128f)



