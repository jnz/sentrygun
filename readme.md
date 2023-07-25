YOLO SENTRY
===========

Basic Idea
----------

The basic idea is that a simple Python script is reading in frames from a
webcam, the tries to detect objects within that image.  If a certain object
class is found, a command is sent to an Arduino board that is controlling an
actuator, i.e. a servo connected to a water pistol.
You can use this to fend away birds, cats, people, etc.




       ┌──────────────────────┐                           ┌────────────────────┐     ┌──────┐
       │                      │   Webcam Frame            │                    │    ┌┘      │
       │  sentry.py           ◄───────────────────────────┤                    ├────┘       │
       │                      │        USB                │    Webcam          │            │
       │                      │                           │                    │            │
       │  Running on a PC     │                           │                    ├────┐       │
       │                      │                           │                    │    └┐      │
       │                      │                           │                    │     └──────┘
       └───────────────┬──────┘                           └────────────────────┘
                       │
                       │ /dev/ttyACMXX USB serial
                       │                                  ┌─────────────────────┐
                       │                                  │                     ├──┐  Water
                       │                                  │   Water Pistol      │  ├───────────────►
                       ▼                                  │                     ├──┘
               ┌────────────────┐                         └─┬─────┬──┬──┬───────┘
               │                │                           │     │  │  │
               │                │                           │     └──┴──┤
               │  Arduino       ├───────────────────────────┼─────►Servo│
               │                │                           │     ┌─────┘
               │                │                           └─────┘
               └────────────────┘

Pictures
--------

![Water Pistol](img/waterpistol.jpg)
![Arduino](img/arduino.jpg)
![GIF](img/person.gif)

Installation
------------

Install the required Python modules (assuming Python 3 is installed on your system):

    pip install pyserial
    pip install opencv-python
    pip install numpy

Download the YOLOv3 network:

    wget https://pjreddie.com/media/files/yolov3.weights
    wget https://github.com/pjreddie/darknet/blob/master/data/coco.names
    wget https://github.com/pjreddie/darknet/raw/master/cfg/yolov3.cfg

Download the Arduino IDE

    https://www.arduino.cc/en/software

Upload the Arduino sketch in the following subfolder to your Arduino board:

    arduino_sentry/arduino_sentry.ino

Connect the Arduino via USB to your computer. Check the serial port, it should normally be something like

    /dev/ttyACM0

If not, modify sentry.py and adjust the following variable:

    TRIGGER_SERIAL

Run the main script:

    python3 sentry.py

Bill of material (BOM)
----------------------

    - Arduino Board. I'm using a M0 Pro, but probably any Arduino that can control a servo should work.
    - [Electric Water Pistol](https://www.amazon.de/-/en/Electric-Automatic-Splasher-Children-Powered/dp/B0C6XPT425/)
    - Webcam. Most USB webcams should work.
    - A servo motor with PWM control
    - Two cable ties to attach the servo motor to the trigger of the water pistol


Other
-----

Another improvement would be the direct control of the trigger pins. Then no servo motor is required.
![Water pistol trigger](img/water_pistol_open.jpg)
![Water pistol trigger zoom](img/waterpistol_open_zoom.jpg)

