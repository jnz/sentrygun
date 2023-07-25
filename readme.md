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

Bill of material (BOM)
----------------------

 - Arduino Board. I'm using a M0 Pro, but probably any Arduino that can control a servo should work.
 - [Electric Water Pistol](https://www.amazon.de/-/en/Electric-Automatic-Splasher-Children-Powered/dp/B0C6XPT425/)
 - Webcam. Most USB webcams should work.


