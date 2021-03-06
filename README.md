# UMD MATES Quick Start Guide

Here is what to expect in this guide: First the radar operator&#39;s gear will be prepared, then the field operator&#39;s, next the iPads will be prepared, and last an operator can choose to wear the equipment and operate it. **ORDER MATTERS.** _Words in italics describe what is going on in the software._


## Attention: Before Setup

During the removal of the AVMU at the competition, the router's epoxy broke and it is now loose in the pelican case. Caution is advised to avoid damage to the contents of the case.

The Mini USB B port on the Wolfhound Pro has the cable hot glued into place. This is because it was not designed to be plugged in and transported simultaneously. Removing the glue may damage the USB port, do so at your own risk.

## Radar Operator

![alt text](media/internals.jpg)

Figure 1: Orientation of the Radar Operator's Pelican Case and Components Inside.


1. Orient the pelican case as shown in Figure 1. Open the case.
2. Lift off wooden radar antenna mounting plate to reveal other components.
3. Power on the battery velcroed into the pelican case. If the battery is not charged, you may not proceed with the procedure until it is charged. When the battery is powered on you should see lights blinking on the router and later hear the fan on the beagle board spinning. Do not tip or jostle around pelican case.
4. On a separate computer (or the supplied iPad with the Terminus app installed), connect to the Wifi network `NETGEAR65` with password `orangeonion830`
5. In an SSH client on that computer, enter the following commands:
       
       ssh debian@192.168.1.7
    
    When prompted for a password, enter `temppwd`
    ```
    cd ~/devices/beagle_avmu_py/src
    python3 BeagleAvmu.py
    ```

_The router provides the local area network (LAN) that the devices connect to. Sensor data is transported from the sensors through the LAN and onto the User Interface.  If the AVMU was still there the Beagle Board would start collecting data from the AVMU on powerup._

1. Once components are powered on, while maintaining current orientation close pelican case, and set the Pelican case aside.

## Field Operator

![alt text](media/fannypack.jpg)
Figure 2: Field Operator&#39;s Lumbar Pack and Components Inside.

![alt text](media/snakescope_parts.png)
Figure 3: Names of SnakeScope Components

1. Check the power level of the large black USB power pack and the two white smaller power packs. They were left in the lumbar pack at the university. If they are not charged you may not proceed with the procedure until it is charged.
2. Before powering on the field operators Raspberry Pi, plug in (if not plugged in already):
   1. the Phone Detector in one of the Raspberry Pi&#39;s USBs. **Be mindful of the hot glue seal.**
   2. the SnakeScope camera in one of the Raspberry Pi&#39;s USBs
   3. the SnakeScope Microphone Input in one of the Raspberry Pi&#39;s USBs
   4. the SnakeScope Microphone Input&#39;s two power cables, plug each one into its own small white power pack. Note the picture above shows one of the microphone cables connected to the black power supply but now each microphone power cable gets its own white power pack.
   5. the headphones into the Raspberry Pi&#39;s Auxiliary Port
   6.  the power cable for the Raspberry Pi&#39;s into the large black USB Power Supply
3. Place the headphones in your ears.
4. Power on the Phone Detector by pressing the black button in the middle of the key pad. You should see a screen similar to this below…

![alt text](media/phone_detector_default.png)

Figure 4: Phone Detector Default

If the phone detector is not charged, you may not proceed with the procedure until it is charged.

1. Power on the Raspberry Pi by pressing the button on the power cord. As the Raspberry Pi is turning on you will start to hear sound coming from the headphones and the Phone Detector will display the text "USB Control"

_As the Raspberry Pi powers on three services run. The first starts the microphone collection, the second starts the Phone Detector data collection/ transportation, and the third starts the SnakeScope data collection/ transportation._

**Motion Detector**

1. Flip on the motion detector sensor so the switch is pointed to the green color. Flip on the motion detector receiver (connected to the glasses) so that the switch is pointed to the green color. In a few moments you should see the sensor and the glasses&#39; lights blink as motion is being detected.

_As the Motion Detector powers on it connects to the LAN so that the data can be shared to the receiver (glasses) and User Interface. Therefore, the Motion Detector sensor cannot communicate to the glasses without the LAN on, located in the Radar Operator&#39;s pelican case._



## iPads

1. Power on an iPad. If the iPad is not charged, you may not proceed with the procedure until it is charged.
2. Navigate to the iPad&#39;s wifi options and make sure it is connected to `NETGEAR65` this is the local area network being broadcasted. If you are prompted for a password it is  &quot;orangeonion830&quot;.
3. Navigate to the iPad&#39;s Safari options in settings, scroll down, and click the blue &quot;clear all&quot; button.
4. Open Safari and type in the web bar &quot;192.168.1.7:8080&quot; this is the web address of the user interface being hosted by the beagle board. You should see on the iPad what is shown in Figure 5.


![alt text](media/user_interface.JPG)
Figure 5: Working User Interface









## Wearing the Equipment

Shown in Figure 6 is how the equipment is worn by the field operator. Without the AVMU in the Radar Operator&#39;s pelican case, the pelican case is solely there to provide the LAN and the User Interface.
![alt text](media/field_operator_gear_on.jpg)
Figure 6: Field Operator with all Equipment Mounted

# Troubleshooting
**The Cellphone Detector does not display "USB Control"**
1. Ensure USB cable from the cellphone detector is plugged into raspberry pi
2. If off, turn on the cellphone detector
3. Restart the raspberry pi using the power button on the power cable

**The LED on the glasses does not blink**
1. Turn off the glasses and the motion sensor
2. Ensure NETGEAR65 is listed as an available WiFi network
3. Turn on motion detector and wait for green light on top to blink
4. Turn on the glasses

**The server running on the BeagleBoard crashes**
**If the UI is not reachable on the iPad, follow these steps**
1. In an SSH client on that computer, enter the following commands:
       
       ssh debian@192.168.1.7
    
2. When prompted for a password, enter `temppwd`
3. When the prompt appears, enter the following commands
    ```
    cd ~/devices/beagle_avmu_py/src
    killall python3
    python3 BeagleAvmu.py
    ```
3. Refresh the page on the iPad
